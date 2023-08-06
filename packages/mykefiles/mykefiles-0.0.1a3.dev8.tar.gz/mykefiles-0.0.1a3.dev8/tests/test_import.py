import myke


def test_import():
    myke.TASKS.clear()

    from mykefiles import hello_world  # noqa, pylint: disable=unused-import

    assert "hello" in myke.TASKS
