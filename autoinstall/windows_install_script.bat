TITLE Installing PRISMA
ECHO Creating conda environment ...
call %USERPROFILE%/Miniconda3/Scripts/activate.bat
call cd ..
call conda env create --file requirements.yml
ECHO Activating environment ...
call conda activate prisma
ECHO Installing prisma package ...
call pip install . --user
ECHO Creating Jupyter kernel ...
ipython kernel install --user --name=prisma
call conda deactivate
ECHO Installation complete!
exit
