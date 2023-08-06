from checksome import __version__
from checksome.cli import ChecksomeCli


def entry() -> None:
    ChecksomeCli.invoke_and_exit(app_version=__version__)


if __name__ == "__main__":
    entry()
