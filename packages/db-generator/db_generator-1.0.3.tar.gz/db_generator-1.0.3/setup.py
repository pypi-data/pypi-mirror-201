from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))


long_description = '''

#Use for

This project allows user to define json structure for creating sqlite3 
database as defined in the json file.

#Use the following code


import os
from src.main import main

def generator():
    To generate the schema for us
    sr = input('Enter your source of json file> ')
    dis = input('Enter your destination for .db file> ')
    main(sr, dis)

if __name__ == '__main__':
    generator()

# make sure

that the json structure is same as the given structure.
Have following project structure

your project
    |
    |json_folder
        |
        |json_files
    main.py 


'''

VERSION = '1.0.3'
DESCRIPTION = 'A package which will create sqlite3 database code by configuring them in json file'
LONG_DESCRIPTION = 'A package which will create sqlite3 database code by configuring them in json file'

# Setting up
setup(
    name="db_generator",
    version=VERSION,
    author="Ganesh Yatesh Joshi",
    author_email="ganesh.22110724@viit.ac.in",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'database', 'json configuration for database', 'json', 'sqlite3', 'mobile database'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)