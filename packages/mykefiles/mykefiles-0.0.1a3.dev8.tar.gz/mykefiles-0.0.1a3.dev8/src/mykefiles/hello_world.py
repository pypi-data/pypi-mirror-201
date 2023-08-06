import myke


@myke.task
def hello(name: str = "world", upper: bool = False) -> None:
    """this function will say hello to <name> with optional uppercasing

    Args:
        name: Defaults to "world".
        upper: Defaults to False.
    """
    msg: str = f"hello {name}"
    myke.echo(msg.upper() if upper else msg)
