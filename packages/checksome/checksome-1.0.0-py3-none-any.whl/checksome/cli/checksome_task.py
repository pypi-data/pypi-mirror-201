from cline import CommandLineArguments, Task

from checksome.algorithms import get_algorithm
from checksome.checks import checksum_reader
from checksome.cli.args import TaskArgs


class ChecksomeTask(Task[TaskArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> TaskArgs:
        return TaskArgs(
            algorithm=get_algorithm(args.get_string("algorithm")),
            source=args.get_string("source"),
        )

    def invoke(self) -> int:
        with checksum_reader(self.args.source, self.args.algorithm) as cf:
            self.out.write(cf.checksum().hex())
            self.out.write("\n")

        return 0
