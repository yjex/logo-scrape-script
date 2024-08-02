:: Getting Batch File Location Directory - Relative Path
set script_dir=%~dp0

:: Changing to Python Script Directory
cd /d %script_dir%

@echo off
:: This batch file runs the following packages:
:: main.py -> Pulls data from links indicated in worksheet cells and updates it into the corresponding cells
:: **IMPORTANT** Ensure that the two following files are in the same folder as the logopull.bat file: main.py, env.py

@echo Running main.py
python main.py

@echo The programme has finished running. You can close this window.
pause