import enum
import argparse
import contextlib
from pathlib import Path
from dataclasses import dataclass
from typing import Self


class Mode(enum.Enum):
    BUILD = "build"
    SELECT = "select"
    INJECT = "inject"


@dataclass
class Arguments(argparse.Namespace):
    mode: Mode
    source: str | None = None
    build: str | None = None
    skin: str | None = None

    @classmethod
    def from_argv(cls) -> Self:
        parser = argparse.ArgumentParser(description="Creates osu mania skins for various key counts")

        parser.set_defaults(mode=Mode.SELECT)

        subparsers = parser.add_subparsers(help="mode")

        build_mode = subparsers.add_parser("build")
        build_mode.set_defaults(mode=Mode.BUILD)
        build_mode.add_argument("source")

        inject_mode = subparsers.add_parser("inject")
        inject_mode.set_defaults(mode=Mode.INJECT)
        inject_mode.add_argument("build")
        inject_mode.add_argument("skin")

        return cls(**dict(parser.parse_args()._get_kwargs()))


def select(choices: list[str]):
    for i, choice in enumerate(choices, 1):
        print(f"{i}) {choice}")

    choice = None

    while choice not in range(len(choices)):
        with contextlib.suppress(ValueError):
            choice = int(input("> ")) - 1

    assert isinstance(choice, int)

    return choices[choice]


def select_dir(select_path: Path | str) -> Path:
    select_path = Path(select_path)
    directories = {p.name: p for p in select_path.iterdir() if p.is_dir()}
    return directories[select(list(directories))]
