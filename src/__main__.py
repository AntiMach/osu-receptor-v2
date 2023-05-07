import sys
import argparse
import enum
from pathlib import Path

from src.build import build_skin
from src.const import BUILD_DIR, SOURCE_DIR
from src.inject import from_osu_install, get_osu_install, inject_build_replace


class Mode(enum.Enum):
    BUILD = enum.auto()
    SELECT = enum.auto()
    INJECT = enum.auto()


def main():
    cmd, *args = sys.argv

    parser = argparse.ArgumentParser(
        cmd, description="Creates osu mania skins for various key counts"
    )

    parser.set_defaults(mode=Mode.SELECT)

    subparsers = parser.add_subparsers(help="mode")

    build_mode = subparsers.add_parser("build")
    build_mode.set_defaults(mode=Mode.BUILD)
    build_mode.add_argument(
        "-s", "--source", dest="source", type=str, default=Mode.SELECT
    )

    inject_mode = subparsers.add_parser("inject")
    inject_mode.set_defaults(mode=Mode.INJECT)
    inject_mode.add_argument(
        "-b", "--build", dest="build", type=str, default=Mode.SELECT
    )
    inject_mode.add_argument(
        "-s", "--skin", dest="skin", type=str, default=Mode.SELECT
    )

    args = parser.parse_args(args)

    if args.mode == Mode.SELECT:
        run_select()

    elif args.mode == Mode.BUILD:
        run_build(args.source)

    elif args.mode == Mode.INJECT:
        run_inject(args.build, args.skin)


def select(choices):
    for i, choice in enumerate(choices, 1):
        print(f"{i}) {choice}")

    choice = None

    while choice not in range(len(choices)):
        try:
            choice = int(input("> ")) - 1
        except ValueError:
            choice = None

    return choices[choice]


def select_dir(select_path) -> Path:
    select_path = Path(select_path)
    directories = [p.name for p in select_path.iterdir() if p.is_dir()]
    return select(directories)


def run_select():
    print("Select mode to run:")
    choice = select(["build", "inject"])
    print()

    if choice == "build":
        run_build(Mode.SELECT)
    else:
        run_inject(Mode.SELECT, Mode.SELECT)


def run_build(source: Mode | str):
    if source == Mode.SELECT:
        print("Select source to build:")
        source = select_dir(SOURCE_DIR)

    print()
    print(f"Building {source}...")
    build_skin(source)


def run_inject(build: Mode | str, skin: Mode | str):
    if build == Mode.SELECT:
        print("Select build to inject:")
        build = select_dir(BUILD_DIR)

    if skin == Mode.SELECT:
        print("Select skin to inject to:")
        skin = select_dir(get_osu_install())

    print()
    print(f"Injecting {build} onto {skin}...")
    inject_build_replace(build, from_osu_install(skin))


if __name__ == "__main__":
    main()
