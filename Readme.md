![Logo](./docs/figures/logo.png) 
# PRISMA App

PRISMA is a Jupyter-based app for high-throughput analysis of spectra. The app addresses the need of researchers working in spectroscopy to analyze large numbers of spectra quickly, simply and reproducibly - whether they are code-savvy or not. PRISMA consists of both Python-based code for analysis of spectra and a user-friendly Graphical User Interface (GUI) built with the ipywidgets module.   

# Cite
Please cite this article if you use the app and/or the package:  
>Eibar Flores, Nataliia Mozhzhukhina, Xinyu Li, Poul Norby, Aleksandar Matic,Tejs Vegge.  PRISMA: A robust and intuitive tool for high-throughput processing of chemical spectra. ChemRxiv. [Preprint.] October, 2021. DOI: 10.33774/chemrxiv-2021-7qs3m

# License
PRISMA is distributed under an **Open Source BSD 3-Clause 'New' or 'Revised' License**. This License is similar to the BSD 2-Clause License, but with a 3rd clause that prohibits others from using the name of the project or its contributors to promote derived products without written consent. In short:  
### Permissions 
* Commercial use
* Modification
* Distribution
* Private use
 ### Limitations 
* Liability
* Warranty
 ### Conditions 
* License and copyright notice  

See [here](https://choosealicense.com/licenses/bsd-3-clause/) for more information about this license.



# Installation
## Click-and-play installation
For users unfamiliar with Python and code, we have prepared some scripts that install all necessary tools to run PRISMA's App. Here are detailed instructions: 

* First download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Miniconda is a Python distribution (Python + other useful tools) that enables to run Python code, manage and install third-party packages. Miniconda is conveninent to quickly set up everything you need to run Python programs, including PRISMA.
> **Note**: Make sure that Miniconda installs in the default folder `C:\Users\your_user_name\Miniconda3`. This will enable installing PRISMA smoothly.
* In this github page click on the green button *Code* and Download ZIP
* Unzip the file and open the folder. There you will find a bunch of files that contain code (prisma folder), documentation and examples (docs folder), scripts etc.
* Navigate to the [autoinstall](./autoinstall) folder and double click *windows_install_script.bat* file. A terminal (small black window with Matrix-style fonts) will appear and run the commands automatically. Just wait until it closes alone. This file will automatically run the necessary commmands to set up PRISMA.  

Thats it! You are ready to go. To launch the app, go back to the main folder and double-click on *launch_prisma.bat*. A browser tab will open and load the app. You can click the same *launch_prisma.bat* file every time you wish to use the app.

**Problems with the automated installation? Familiar with Python?**   

If you encounter problems with the manual installation and/or are familiar with Python, you can install PRISMA 'manually'. 
>**Note for Python savvy users**: While this is an operating version of PRISMA, we are still working in a stable version without package incompatibilities, that we can release to Pypi and/or Anaconda. In the meantime, you can try the 'manual' installation.

**'Manual' installation**
* Download/Clone the repository.
* Create a conda environment based on the *requirements.yml* file. 
* Activate the created environment and install prisma from the root directory (where the setup file is) using `pip install .`. If you have an installation error, try running the command prompt as administrator, or if you cannot, run `pip install . --user`. See [this post](https://www.dev2qa.com/how-to-fix-could-not-install-packages-due-to-an-environmenterror-winerror-5-access-is-denied-error-when-install-python-module-in-windows/) for more details.
* If you wish to use PRISMA from Jupyter or use the GUI as well, make sure to install a PRISMA jupyter kernel as well. Run the following command after activating prisma's conda environment: `ipython kernel install --user --name=prisma`. Now you will be able to use prisma from Jupyter Lab, either to use it as a package or to run its GUI [GUI.ipynb](./gui).  

>**Note:** These steps are automated in the scritps provided in the [autoinstall](./autoinstall) directory

In the following links you can find more information about [jupyter kernels](https://ipython.readthedocs.io/en/stable/install/kernel_install.html) and [how to manage them](https://queirozf.com/entries/jupyter-kernels-how-to-add-change-remove).



>**Note for Python savvy users** Conda is used as environment manager and Python distribution because we found it to be the easiest way to install PRISMA in PCs with no admin rights, which is the case in many academic institutions. Some PCs do not even allow to install vanilla Python without admin rights. A compiled .exe is even more difficult to install. To our knowledge, there is no way easier than CONDA to go from developing Python source code to deploying in an user's PC; but we are always open to new ideas, developements and suggestions.

# Use: as an app
The general workflow to use the app consist of i) choosing a pipeline (i.e. a series of processing steps), ii) exploring processing parameters and iii) running a high-throughput analysis applying the same parameters to all spectra. These three steps are divided as tabs in the GUI. The illustration below shows an example of typical steps when performing baseline substraction followed by peak fitting:


![General Workflow](./docs/figures/app_use.png)  

Consult the [App use](./docs) in the documentation for a complete description of these steps, potential issues and suggested workarounds.  


# Use: as a package
We have created a jupyter notebook with examples of how to use all prisma functionalities as a package. You can find the examples and complete documentation in the [docs](./docs). If you wish to run the [examples.ipynb](./docs/examples.ipynb) make sure to have installed a prisma jupyter kernel as specified above.




# Contact
Eibar Flores  
Technical University Denmark  
eibfl@dtu.dk


