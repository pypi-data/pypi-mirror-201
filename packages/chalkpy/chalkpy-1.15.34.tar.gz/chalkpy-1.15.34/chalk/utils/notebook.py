from typing import Optional


def get_ipython_string() -> Optional[str]:
    """
    :return: "ZMQInteractiveShell" for jupyter notebook, "TerminalInteractiveShell" for ipython in terminal, None otherwise.
    """
    try:
        # I know this has a redline under it... we'll catch the NameError as a Falsy condition below
        # noinspection PyUnresolvedReferences
        shell = get_ipython().__class__.__name__
        return shell
    except NameError:
        return None  # Probably standard Python interpreter


def is_notebook() -> bool:
    """:return: true if run inside a Jupyter notebook"""
    shell = get_ipython_string()
    return shell == "ZMQInteractiveShell"
