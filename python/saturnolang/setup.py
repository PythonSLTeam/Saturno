# Arquivo: python/saturnolang/setup.py
from setuptools import setup
import os
import sys

# Aponta para o caminho onde está o arquivo saturnolang.py (voltando uma pasta e entrando em library)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../library')))

setup(
    name="saturnolang",  # Nome do pacote para o 'pip install'
    version="1.0.0",     # Versão da linguagem da PythonSLTeam
    author="PythonSLTeam",
    description="Uma linguagem de programação embutida chamada Saturno",
    url="https://github.com/PythonSLTeam/Saturno",
    
    # Como o código é um arquivo único (.py) e não uma pasta, usamos py_modules
    py_modules=["saturnolang"],
    
    # Informa ao setup.py onde encontrar o arquivo saturnolang.py
    package_dir={"": "../library"},
    
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
