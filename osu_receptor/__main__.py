from pathlib import Path

from osu_receptor.build import build_skin
from osu_receptor.const import BUILD_DIR, SOURCE_DIR
from osu_receptor.argparse import parse_args, select, select_dir, Mode
from osu_receptor.inject import get_osu_install, inject_build_replace


def main():
    match (args := parse_args()).mode:
        case Mode.SELECT:
            run_select()

        case Mode.BUILD:
            run_build(args.source)

        case Mode.INJECT:
            run_inject(args.build, args.skin)


def run_select():
    print("Select mode to run:")
    choice = select(["build", "inject"])
    print()

    if choice == "build":
        run_build()
    else:
        run_inject()


def run_build(source: str | None = None):
    if not source:
        print("Select source to build:")
        source = select_dir(SOURCE_DIR)

    print()
    print(f"Building {source}...")
    build_skin(source)


def run_inject(build: str | None = None, skin: str | None = None):
    print("Warning! This process will replace existing" "skin elements and skin.ini mania sections!")

    if build:
        build = Path(BUILD_DIR) / build
    else:
        print("Select build to inject:")
        build = select_dir(BUILD_DIR)

    if skin:
        skin = get_osu_install() / skin
    else:
        print("Select skin to inject to:")
        skin = select_dir(get_osu_install())

    print()
    print(f"Injecting {build} onto {skin}...")
    inject_build_replace(build, skin)


if __name__ == "__main__":
    main()
