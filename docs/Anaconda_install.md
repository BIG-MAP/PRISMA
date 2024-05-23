# Installation instructions with Anaconda
Courtesy of Eva Maria del Campo Ortiz and colleagues (Warsaw University of Technology)

Install
1. Download and extract the PRISMA the files anywhere you like, keep a note of this.
2. Launch Anaconda, go to environments on the lefthand side, select Base(root) and click open in terminal.
3. Find the folder which you put the prisma files in. In the terminal navigate to it using "cd 'path to file'", for example - cd C:\PRISMA-main\PRISMA-main
4. In the terminal enter the command - conda env create --name prisma --file=requirements.yml, press enter.
5. In the terminal enter the command - pip install ., press enter. This might take a while.
6. In the terminal enter the command - ipython kernel install --user --name=prisma, press enter.

Launch prisma:
1. Open Anaconda
2. Go to the environments tab and click on prisma
3. Click the arrow and select open terminal
4. In the terminal paste - cd ..\..\PRISMA-main\PRISMA-main\gui, then press enter
5. Again, past - jupyter notebook GUI.ipynb and press enter
6. Click run