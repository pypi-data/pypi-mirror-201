# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 12:29:28 2023

@author: Ronaldo Herlinger Junior
"""

from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Pore-scale Pre-salt model generator'
LONG_DESCRIPTION = '''This package has functions to build 3d pore-scale
                    models to be used in simulations.'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pspsmgen", 
        version=VERSION,
        author="Ronaldo Herlinger Jr",
        author_email="<ronaldohj@hotmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy','scipy','math'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'pore-scale', 'digital rock', 'Pre-salt'],
        classifiers= [           
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        [project.urls]
        "Homepage" = "https://github.com/ronaldohj/pspsmgen"
        ]
)