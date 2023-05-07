@echo off
python -m pip install pyinstaller pillow
pyinstaller --distpath . -y --clean --icon=icon.ico -F main.py
pause