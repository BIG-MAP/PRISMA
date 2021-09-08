TITLE Installing PRISMA
ECHO Creating conda environment ...
call %USERPROFILE%/Miniconda3/Scripts/activate.bat
call conda env create --file requirements.yml
ECHO Activating environment ...
call conda activate prisma
ECHO Creating Jupyter kernel ...
ipython kernel install --user --name=prisma
call conda deactivate
ECHO Installation complete!
exit
