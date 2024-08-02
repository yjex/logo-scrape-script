:: This file should only be run the first time you use logopull.bat
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

python -m pip install --upgrade pip

:: Getting Batch File Location Directory - Relative Path
set script_dir=%~dp0

:: Installation of packages 
cd /d %script_dir%

pip install -r requirements.txt

echo Package installation complete, you can close this window
pause