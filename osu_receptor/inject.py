import os
import shutil
from pathlib import Path

import osu_receptor.const as const


def overwrite_mania_sections(skin_ini: Path, new_data: str):
    result = ""
    is_mania = False

    with skin_ini.open("r", encoding="utf8") as fp:
        for line in fp.readlines():
            normalized_line = line.strip().lower()

            if normalized_line.startswith("["):
                is_mania = normalized_line == "[mania]"

            if not is_mania:
                result += line

    with skin_ini.open("w", encoding="utf8") as fp:
        fp.write(result.rstrip())
        fp.write("\n\n\n")
        fp.write(new_data)


def get_osu_install():
    return Path(os.getenv("LOCALAPPDATA")) / const.OSU_SKIN_DIR


def inject_build_replace(build_dir: Path, skin_dir: Path):
    build_ini = build_dir / const.SKIN_INI
    skin_ini = skin_dir / const.SKIN_INI

    skin_asset_dir = skin_dir / const.ASSET_DIR
    build_asset_dir = build_dir / const.ASSET_DIR

    skin_asset_list_file = skin_asset_dir / const.ASSET_LIST_FILE

    # Overwrite ini file
    overwrite_mania_sections(skin_ini, build_ini.read_text("utf8"))

    # Get list of asset files to remove
    skin_asset_list = []
    if skin_asset_list_file.is_file():
        skin_asset_list = skin_asset_list_file.read_text().splitlines()

    # Remove asset files
    for asset in skin_asset_list:
        (skin_asset_dir / asset).unlink(True)

    # Create list of asset files added
    build_asset_list = []
    for asset in build_asset_dir.iterdir():
        if (skin_asset_dir / asset.name).exists():
            raise FileExistsError(str(asset))

        build_asset_list.append(asset)

    skin_asset_dir.mkdir(exist_ok=True)

    # Copy asset files
    with skin_asset_list_file.open("w", encoding="utf8") as fp:
        for asset in build_asset_list:
            shutil.copy(asset, skin_asset_dir)
            fp.write(f"{asset.name}\n")
