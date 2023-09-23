import contextlib
import enum
import argparse
from pathlib import Path


class Mode(enum.Enum):
    BUILD = enum.auto()
    SELECT = enum.auto()
    INJECT = enum.auto()


class Arguments(argparse.Namespace):
    mode: Mode
    source: str | None
    build: str | None
    skin: str | None


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(description="Creates osu mania skins for various key counts")

    parser.set_defaults(mode=Mode.SELECT)

    subparsers = parser.add_subparsers(help="mode")

    build_mode = subparsers.add_parser("build")
    build_mode.set_defaults(mode=Mode.BUILD)
    build_mode.add_argument("-s", "--source", dest="source")

    inject_mode = subparsers.add_parser("inject")
    inject_mode.set_defaults(mode=Mode.INJECT)
    inject_mode.add_argument("-b", "--build", dest="build")
    inject_mode.add_argument("-s", "--skin", dest="skin")

    return parser.parse_args()


def select(choices: list[str]):
    for i, choice in enumerate(choices, 1):
        print(f"{i}) {choice}")

    choice = None

    while choice not in range(len(choices)):
        with contextlib.suppress(ValueError):
            choice = int(input("> ")) - 1

    return choices[choice]


def select_dir(select_path: Path | str) -> Path:
    select_path = Path(select_path)
    directories = {p.name: p for p in select_path.iterdir() if p.is_dir()}
    return directories[select(directories)]
