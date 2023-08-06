from argparse import ArgumentParser

from cline import ArgumentParserCli, RegisteredTasks

from greas3.cli.greas3_task import Greas3Task


class Greas3Cli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            description=(
                "Greas3 uploads files and directories to Amazon Web Services "
                "S3 like a greased thing."
            ),
            epilog=("See https://cariad.github.io/greas3/ for usage and " "support."),
        )

        parser.add_argument(
            "source",
            help='source path (e.g. "/home/cariad/clowns.jpg")',
        )

        parser.add_argument(
            "destination",
            help='destination URI (e.g. "s3://circus/")',
        )

        parser.add_argument(
            "--dry-run",
            help="perform a dry-run",
            action="store_true",
        )

        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            Greas3Task,
        ]
