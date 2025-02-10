# osu-receptor-v2

## The successor to osu-receptor

This version allows for the creation of covers and percy lns.
Every other feature is still present here.

## Running straight from the repo

You're going to need python 3.12 or higher.

The virtual environment is optional, but recommended!

```sh
# create and activate venv (WINDOWS)
pip install poetry

# create and activate venv (LINUX)
python3.12 -m pip install poetry

# install requirements
poetry install

# run
poetry run python -m osu_receptor
```

## Using an executable

You can get a prepackaged binary in the releases.

To package it yourself, do the following:

```sh
# make the package
poetry run pyinstaller --distpath . -y --clean --icon=icon.ico -F main.py
```

The package should be called `main.exe` on windows, `main` on linux.

## settings.yaml

Check the comments in the `settings.yaml` file for more details.

## Sources

Different skin styles can be created in the `source` folder next to the `osu_receptor` module.

Inside that folder, any subfolder with a `skin.json` file is considered a skin template.

### skin.yaml

Check the comments in the example skin's `skin.yaml` file at `source/example/skin.yaml` for more details.
