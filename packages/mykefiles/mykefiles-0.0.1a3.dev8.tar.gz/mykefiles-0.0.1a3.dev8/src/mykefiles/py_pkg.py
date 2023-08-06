import os
from contextlib import suppress
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import myke
from myke.types import Annotated

PYENV_VERSION_FILE: str = ".python-base-version"
PYENV_VENV_FILE: str = ".python-version"

VERSION_FILE: str = "VERSION"

replace_prefix: str = "DRONE"
replace_with: str = "CI"
for k in list(os.environ.keys()):
    if k.startswith(replace_prefix):
        new_k: str = k.replace(replace_prefix, replace_with, 1)
        if new_k not in os.environ:
            os.environ[new_k] = os.environ[k]

more_alternatives: Dict[str, str] = {"CI_TAG": "CI_COMMIT_TAG"}
for k, v in more_alternatives.items():
    if k in os.environ and v not in os.environ:
        os.environ[v] = os.environ[k]


@myke.cache()
def _get_project_name() -> str:
    proj_name: Optional[str] = None

    if os.path.exists("setup.py"):
        proj_name = myke.sh_stdout("python setup.py --name")

    if not proj_name:
        if os.path.exists("setup.cfg"):
            proj_name = myke.read.cfg("setup.cfg").get("metadata", {}).get("name")

        if not proj_name:
            if os.path.exists(".env"):
                proj_name = myke.read.dotfile(".env").get("COMPOSE_PROJECT_NAME")

            if not proj_name:
                proj_name = os.getenv("CI_REPO_NAME")

                if not proj_name:
                    proj_name = os.path.split(os.getcwd())[-1]

    return proj_name


@myke.cache()
def _get_package_root() -> str:
    default_root: str = "src"

    pkg_root: str = (
        str(
            myke.read.cfg("setup.cfg")
            .get("options.packages.find", {})
            .get("where", default_root),
        )
        if os.path.exists("setup.cfg")
        else default_root
    )

    if not os.path.exists(pkg_root):
        proj_name: Optional[str] = _get_project_name()
        if proj_name and os.path.exists(os.path.join(proj_name, "__init__.py")):
            pkg_root = proj_name
        else:
            pkg_root = os.getcwd()

    return pkg_root


@myke.cache()
def _get_package_dirs() -> List[str]:
    return myke.sh_stdout_lines(
        f"""
    find "{_get_package_root()}" \
        -mindepth 2 -maxdepth 2 -name "__init__.py" -exec dirname {{}} \\;
    """,
    )


def _assert_git(assert_clean: bool = False) -> None:
    stdout = myke.sh_stdout("git status --porcelain").strip()
    if assert_clean:
        assert (
            not stdout
        ), f"Git repository has uncommitted changes; aborting.\n\n{stdout}"


@myke.task_sh
def x_py_which() -> None:
    return "which python"


@myke.task
def x_py_get_version(_echo: bool = True) -> str:
    value: str = myke.sh_stdout("python setup.py --version")
    if _echo:
        print(value)
    return value


def _assert_unpublished(
    repository: Optional[str] = None,
    version: Optional[str] = None,
) -> List[str]:
    vers_published: List[str] = x_py_get_published(repository=repository, _echo=False)

    if not version:
        version = x_py_get_version(_echo=False)

    if version in vers_published:
        raise SystemExit(
            ValueError(f"Version {version} already published; increment to continue."),
        )

    return vers_published


def _get_next_version(
    repository: Optional[str] = None,
    version: Optional[str] = None,
    dev_build: bool = False,
) -> str:
    if not version:
        version = os.getenv("CI_COMMIT_TAG", None)
        if not version:
            if os.path.exists(VERSION_FILE):
                version = myke.read(VERSION_FILE)
            else:
                version = "0.0.1a1"

    vers_published: List[str] = _assert_unpublished(
        repository=repository,
        version=version,
    )
    # if in CI, but no tag, append next '.dev#' to version
    if os.getenv("CI") and not os.getenv("CI_COMMIT_TAG"):
        dev_build = True

    if dev_build:
        max_dev_build: int = max(
            int(dev_i[3:]) if dev_i.startswith("dev") else 0
            for x in vers_published
            for dev_i in [x.rsplit(".")[-1]]
        )
        version += f".dev{max_dev_build+1}"

    if not os.path.exists(VERSION_FILE):
        x_py_set_version(version, _echo=False)

    return version


@myke.task
def x_py_set_version(
    version: Annotated[Optional[str], myke.arg(pos=True)] = None,
    repository: Optional[str] = None,
    commit: bool = False,
    dev_build: bool = False,
    _echo: bool = True,
) -> None:
    if commit:
        _assert_git(assert_clean=True)

    version_og: Optional[str] = None
    with suppress(myke.exceptions.CalledProcessError):
        version_og = x_py_get_version(_echo=False)

    if not version:
        version = _get_next_version(
            version=version,
            repository=repository,
            dev_build=dev_build,
        )

    if version_og != version:
        if _echo:
            print(f"{version_og} --> {version}")
        myke.write(path=VERSION_FILE, content=version + os.linesep, overwrite=True)

        if not os.path.exists("MANIFEST.in"):
            myke.write(path="MANIFEST.in", content=f"include {VERSION_FILE}")

        myke.sh(
            r"sed 's/^version.*/version = file: VERSION/' setup.cfg > setup.cfg.tmp "
            r"&& mv setup.cfg.tmp setup.cfg",
        )

    assert version == x_py_get_version(_echo=False)

    for pkg in _get_package_dirs():
        myke.write(
            content=f'__version__ = "{version}"' + os.linesep,
            path=os.path.join(pkg, "__version__.py"),
            overwrite=True,
        )

    if commit:
        myke.sh(f"git commit -am 'bump: {version}'")


@myke.task_sh
def x_py_clean():
    return (
        f"rm -rf dist build public {_get_package_root()}/*.egg-info .mypy_cache"
        " .pytest_cache .coverage .hypothesis .tox"
    )


@myke.task
def x_py_env(
    version=None,
    name=None,
) -> str:
    x_py_clean()

    x_py_set_version(None)

    if not name:
        name = _get_project_name()

    if version:
        myke.sh(f"pyenv local {version}")
    elif os.path.exists(PYENV_VERSION_FILE):
        os.rename(PYENV_VERSION_FILE, PYENV_VENV_FILE)

    myke.sh(
        f"""
export PYENV_VIRTUALENV_DISABLE_PROMPT=1 \\
&& pyenv virtualenv-delete -f {name} \\
&& pyenv virtualenv {name} \\
&& mv {PYENV_VENV_FILE} {PYENV_VERSION_FILE} \\
&& pyenv local {name}
""",
        env_update={"PYENV_VERSION": None},
    )

    return name


@myke.task
def x_py_requirements(
    extras: Optional[List[str]] = None,
    quiet: bool = False,
    _pyenv_name: Optional[str] = None,
) -> None:
    setup_cfg: Dict[str, Any] = myke.read.cfg("setup.cfg")

    install_requires: List[str] = [
        x
        for x in setup_cfg.get("options", {}).get("install_requires", "").splitlines()
        if x
    ]

    extras_require: Dict[str, str] = setup_cfg.get("options.extras_require", {})

    if extras:
        if not extras_require:
            raise ValueError("Missing value for 'options.extras_require'")
        for e in extras:
            if e not in extras_require:
                raise ValueError(
                    (
                        f"Extra requirement '{e}' not one of: "
                        f"{','.join(extras_require.keys())}"
                    ),
                )

    extra_reqs: List[str] = [
        req
        for grp, reqs in extras_require.items()
        if (not extras or grp in extras)
        for req in reqs.strip().splitlines()
        if req
    ]

    quiet_flag: str = ""
    if quiet:
        quiet_flag = "-q"

    core_reqs: List[str] = ["pip", "setuptools", "wheel"]

    env_update: Dict[str, str] = {}
    if _pyenv_name:
        env_update["PYENV_VERSION"] = _pyenv_name

    for reqs in core_reqs, install_requires, extra_reqs:
        if reqs:
            reqs = [x.replace("'", '"') for x in reqs]
            reqs_str: str = "'" + "' '".join(reqs) + "'"
            myke.sh(
                f"python -m pip install --upgrade {quiet_flag} {reqs_str}",
                env_update=env_update,
            )


@myke.task
def x_py_repos(
    path: Optional[str] = None,
    echo: Annotated[bool, myke.arg(True)] = False,
) -> Dict[str, Dict[str, str]]:
    if not path:
        path = os.path.join(os.path.expanduser("~"), ".pypirc")
    repo_info: Dict[str, Dict[str, str]] = {
        k: v for k, v in myke.read.cfg(path).items() if "username" in v
    }
    if echo:
        myke.echo.lines(list(repo_info.keys()))
    return repo_info


@myke.task
def x_py_get_published(
    repository: str,
    name: Optional[str] = None,
    _echo: bool = True,
) -> List[str]:
    if not name:
        name = _get_project_name()

    pip_args: str = ""
    if repository and repository != "pypi":
        pypi_conf: Dict[str, Dict[str, str]] = x_py_repos()
        if repository not in pypi_conf:
            raise ValueError(
                f"Specified repo '{repository}' not one of: {list(pypi_conf.keys())}",
            )
        repo_key: str = "repository"
        repo_url: Optional[str] = pypi_conf.pop(repository).get(repo_key)
        if not repo_url:
            raise ValueError(
                f"Specified repo '{repository}' has no property '{repo_key}'",
            )

        pip_args = (
            f"--trusted-host '{urlparse(repo_url).netloc}' --index-url"
            f" '{repo_url}/simple'"
        )

    values: List[str] = myke.sh_stdout_lines(
        f"python -m pip install --disable-pip-version-check {pip_args} {name}== 2>&1"
        r" | tr ' ' '\n' | tr -d ',' | tr -d ')' | grep '^v\?[[:digit:]]'"
        r" || true",
    )

    if _echo:
        myke.echo.lines(values)

    return values


@myke.task_sh
def x_py_format() -> str:
    pkg_root: str = _get_package_root()

    py_dirs: List[str] = [pkg_root]

    tests_root: str = "tests"
    if os.path.exists(tests_root) and not os.path.abspath(tests_root).startswith(
        pkg_root,
    ):
        py_dirs.append(tests_root)

    py_dirs_joined: str = " ".join(py_dirs)

    return f"""
echo '*** ruff:'
python -m ruff check --fix-only {py_dirs_joined}
echo '*** isort:'
python -m isort {py_dirs_joined}
echo '*** black:'
python -m black --preview {py_dirs_joined}
"""


@myke.task_sh
def x_py_check(
    critical: Annotated[Optional[bool], myke.arg(exclusive=True)] = None,
    fix: Annotated[Optional[bool], myke.arg(exclusive=True)] = None,
) -> str:
    dirs: List[str] = [_get_package_root()]
    if os.path.exists("./tests"):
        dirs.append("./tests")
    joined_dirs = " ".join(dirs)

    if fix:
        x_py_format()

    if critical:
        return f"""
        echo '*** pylint:'
        python -m pylint --disable=C,R -f colorized {joined_dirs}
        """

    return f"""
echo '*** ruff:'
python -m ruff check {joined_dirs}
echo '*** pylint:'
python -m pylint -f colorized {joined_dirs} || true
echo '*** mypy:'
python -m mypy --install-types --non-interactive || true
"""


@myke.task
def x_py_test(
    *args: str,
    reports: bool = False,
    no_pylint: bool = False,
    no_doctest: bool = False,
) -> None:
    pytest_args: List[str] = list(args)

    if reports:
        pytest_args.extend(
            [
                "--cov-report",
                "xml:public/tests/coverage.xml",
                "--cov-report",
                "html:public/tests/coverage",
                "--html",
                "public/tests/index.html",
            ],
        )

    pkg_root: str = _get_package_root()

    myke.run(
        [
            "python",
            "-m",
            "pytest",
            "--cov=src",
            "--cov-report",
            "term",
            "--durations=10",
            *pytest_args,
        ],
        env_update={"PYTHONPATH": pkg_root},
    )

    #  myke.sh(
    #      (
    #          f"PYTHONPATH={pkg_root} python -m pytest --cov=src"
    #          f" --cov-report term --durations=10 {pytest_args}"
    #      ),
    #  )
    if not no_doctest:
        myke.run(
            [
                "python",
                "-m",
                "pytest",
                "--doctest-modules",
                "--suppress-no-test-exit-code",
                pkg_root,
                *pytest_args,
            ],
            env_update={"PYTHONPATH": pkg_root},
        )
        #  myke.sh(
        #      (
        #          f"PYTHONPATH={pkg_root} python -m pytest --doctest-modules"
        #          f" --suppress-no-test-exit-code {pkg_root}"
        #      ),
        #  )

    if not no_pylint:
        x_py_check(critical=True)


def _get_pyenv_versions() -> List[str]:
    return [
        x for x in myke.sh_stdout_lines("pyenv versions") if myke.utils.is_version(x)
    ]


@myke.task
def x_py_test_tox(*args) -> None:
    py_vers: List[str] = _get_pyenv_versions()
    # TODO: unsure why this is necessary for tox to find python 3.11.0
    py_vers.reverse()

    myke.run(
        ["tox", *args],
        env_update={"PYENV_VERSION": ":".join(py_vers)},
    )


@myke.task
def x_py_mkdocs(
    config: str = "config/mkdocs.yml",
    serve: bool = False,
):
    vip_file_map: Dict[str, str] = {
        "README.md": "docs/index.md",
        "LICENSE": "docs/license.md",
        "CHANGELOG.md": "docs/changelog.md",
        "CONTRIBUTING.md": "docs/contributing.md",
    }

    try:
        for src_file, tgt_link in vip_file_map.items():
            if os.path.exists(src_file):
                myke.sh(f'ln -s "$(realpath {src_file})" "{tgt_link}"')

        myke.sh(
            (
                "python -m mkdocs"
                f" {'serve' if serve else 'build --clean'} --config-file '{config}'"
            ),
            env_update={"PYTHONPATH": _get_package_root()},
        )
    finally:
        for tgt_link in vip_file_map.values():
            if os.path.exists(tgt_link):
                os.unlink(tgt_link)


@myke.task
def x_py_sloc() -> None:
    pkg_root: str = _get_package_root()

    results: List[Dict[str, Union[str, int]]] = []

    for d in (*_get_package_dirs(), "tests"):
        pylint_report: List[str] = myke.sh_stdout_lines(
            f"python -m pylint --disable all --reports=y '{d}'",
            env_update={
                "PYTHONPATH": pkg_root,
            },
        )

        this_dir_result: Dict[str, Union[str, int]] = {
            "Directory": d,
            "Empty": -1,
            "Comment": -1,
            "Docstring": -1,
            "Code": -1,
            "Statements": -1,
        }

        idx: int = pylint_report.index("Report")
        this_dir_result["Statements"] = int(
            pylint_report[idx + 2].split(maxsplit=1)[0],
        )

        idx = pylint_report.index("Raw metrics")
        idx += 3
        this_row: str = pylint_report[idx]
        while this_row.startswith("|"):
            row_split: List[str] = [
                x.strip() for x in this_row.split("|", maxsplit=3) if x
            ]
            if row_split[1].isnumeric():
                this_dir_result[row_split[0].capitalize()] = int(row_split[1])

            idx += 2
            this_row = pylint_report[idx]

        results.append(this_dir_result)

    myke.echo.table(results, tablefmt="github")


@myke.task
def x_py_reports() -> None:
    x_py_clean()
    x_py_mkdocs()
    x_py_test(reports=True)


@myke.task
def x_py_build() -> str:
    x_py_requirements(extras=["build"])

    return myke.sh(r"""
rm -rf dist/
python -m build
python -m twine check --strict dist/*
python -m pip install --force-reinstall dist/*.whl
""")


@myke.task
def x_py_publish(
    repository: Optional[List[str]] = None,
    build: bool = False,
    dev_build: bool = False,
) -> str:
    if not repository:
        repository = list(x_py_repos().keys())

    if build or dev_build:
        x_py_set_version(repository=repository[0], dev_build=dev_build, _echo=False)
        build = True

    if not os.path.exists("dist"):
        build = True

    if build:
        x_py_build()

    default_cert: str = "/etc/ssl/certs/ca-certificates.crt"

    for repo in repository:
        myke.sh(
            f"""
    python -m twine upload --verbose --non-interactive -r {repo} dist/*
    """,
            env_update=(
                {"TWINE_CERT": default_cert}
                if not os.getenv("TWINE_CERT") and os.path.exists(default_cert)
                else {}
            ),
        )


if __name__ == "__main__":
    myke.main(__file__)
