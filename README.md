# osu-receptor-v2

## The successor to osu-receptor

This version allows for the creation of covers and percy lns.
Every other feature is still present here.

## Running straight from the repo

You're going to need python 3.11 or later.

The virtual environment is optional, but recommended!

```sh
# create and activate venv (WINDOWS)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# create and activate venv (LINUX)
python3.11 -m venv .venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# run
python -m osu_receptor
```

## Using an executable

You can get a prepackaged binary in the releases.

To package it yourself, do the following:

```sh
# activate venv (WINDOWS)
.\.venv\Scripts\Activate.ps1

# activate venv (LINUX)
source .venv/bin/activate

# install pyinstaller
pip install pyinstaller

# make the package
pyinstaller --distpath . -y --clean --icon=icon.ico -F main.py
```

The package should be called `main.exe` on windows, `main` on linux.

## settings.json

These define every general setting for your skins.

Settings not marked as **optional** are **required**!

```json
{
    "default": {                // the default settings
        "width": 66,            // the width of columns
        "spacing": 2,           // the spacing between each column
        "hitpos": 60,           // the hit position counting from below, not above like in skin.ini
        "centered": [16, 9],    // (optional) the aspect ratio to center the notefield
        "cover": 64,            // (optional) the height of the note cover (0-480)
        "percy_height": 40000,  // (optional) the height of the percy long notes (0-inf)
        "template": {           // (optional) fields to include in the skin.ini
            "ScorePosition": "200",
            "ComboPosition": "160",
            "SpecialStyle": "0",
            "UpsideDown": "0",
            "JudgementLine": "0",
            "KeysUnderNotes": "1",
            "BarlineHeight": "0",
            "ColourColumnLine": "0,0,0,0",
            "Hit300g": null,                // elements marked as null are replaced with
            "StageHint": null,              // an empty image (blank)
            "StageLight": null,
            "LightingN": null,
            "LightingL": null,
            "Lighting": null,
            "StageLeft": null,
            "StageRight": null
        }
    },
    "<override>": {             // (optional) can have any name, will override default settings
        "keys": [6, 7, 8, 9],   // specify which key counts this override effects
        "width": 56             // (optional) any field above is applicable, but optional!
    }
}
```

## Sources

Different skin styles can be created in the `source` folder next to the `osu_receptor` module.

Inside that folder, any subfolder with a `skin.json` file is considered a skin template.

### skin.json

Should be structured like so:

```json
{
    "columns": {                        // the column templates
        "default": {                    // the default template
            "notetail": true,           // if the tail is a note or a cap
            "color": [0, 0, 0, 240],    // the color of the background
            "keyup": "keyup",           // the keyup asset's name
            "keydown": "keydown",       // the keydown asset's name
            "note": "note1",            // the note asset's name
            "head": "note1",            // the head asset's name
            "body": "body1",            // the body asset's name
            "tail": "tail1"             // the tail asset's name
        },
        "2": {                          // (optional) an override template, must be 1 character
            "note": "note2",            // (optional) any override field is optional and can
            "head": "note2",                // include the same fields as the default
            "body": "body2",
            "tail": "tail2"
        },
        "3": {
            "note": "note3",
            "head": "note3",
            "body": "body3",
            "tail": "tail3"
        },
        "4": {
            "note": "note4",
            "head": "note4",
            "body": "body4",
            "tail": "tail4"
        }
    },
    "layouts": [                        // custom column layouts for each key count
        "3",                            // (optional) the number of characters defines
        "11",                               // the key count, and the characters
        "131",                              // represent the column template to
        "1221",                             // use for each column.
        "12321",                            // Characters not specified use the
        "121121",                           // default template
        "1213121",
        "41213121",
        "121232121"
    ]
}
```
