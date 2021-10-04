# © Copyright 2021, PRISMA’s Authors

from setuptools import setup


setup(
    name='prisma',
    version='0.1.0',
    author='Eibar Flores',
    author_email='eibfl@dtu.dk',
    packages=['prisma'],
    url='https://github.com/eibfl-dtu/PRISMA',
    license='LICENSE.txt',
    description='A robust and intuitive tool for high-throughput processing of spectra',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.20.0",
        "scipy >= 1.6.0",
        "pandas >= 1.2.1",
        "jupyterlab == 3.0.6",
        "ipywidgets == 7.6.3",
        "bqplot == 0.12.21",
        "voila == 0.2.8",
    ],
    entry_points = {
        'console_scripts': [
            'prismaapp = prisma.__main__:main'
        ]
    } #Creates a simple CLI: links to a script to launch the GUI from the command line
)