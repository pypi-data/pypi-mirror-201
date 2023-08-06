from argparse import ArgumentParser

from cline import ArgumentParserCli, RegisteredTasks

from checksome.cli.checksome_task import ChecksomeTask


class ChecksomeCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            description="Checksome generates file checksums.",
            epilog="See https://cariad.github.io/checksome/ for usage and support.",
        )

        parser.add_argument("source", help="source path")
        parser.add_argument("algorithm", help='hash algorithm (e.g. "sha256")')

        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            ChecksomeTask,
        ]
