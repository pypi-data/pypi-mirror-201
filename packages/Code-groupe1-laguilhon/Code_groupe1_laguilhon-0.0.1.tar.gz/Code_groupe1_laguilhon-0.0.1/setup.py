from setuptools import setup, find_packages

from setuptools.command.install import install
import subprocess

setup(
    name="Code_groupe1_laguilhon",
    version="0.0.01",
    author="laguilhon",
    author_email="lea.aguilhon@gmail.com",
    description="Développement logiciel",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OririPla/Dev-logiciel-final.git",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,

    packages=["src/Code","src/Code/docs","src/Code/docs/build","src/Code/docs/source","src/Code/docs/build/doctrees","src/Code/docs/build/html","src/Code/docs/build/html/_modules","src/Code/docs/build/html/_sources","src/Code/docs/build/html/_static","src/Code/docs/build/html/_static/css","src/Code/docs/build/html/_static/css/fonts","src/Code/docs/build/html/_static/fonts","src/Code/docs/build/html/_static/fonts/calcutta","src/Code/docs/build/html/_static/fonts/Lato","src/Code/docs/build/html/_static/fonts/RobotoSlab","src/Code/docs/build/html/_static/js"],

    install_requires=[
        "numpy==1.23.0",
        "pandas>=1.3.3",
        "matplotlib>=3.4.3",
        "scikit-learn>=1.0",
        "scipy==1.9.0",
        "tensorflow>=2.6.0",
        "keras>=2.6.0",
        "opencv-python-headless>=4.5.4.58",
        "pillow>=8.3.2",
        "fpdf>=1.7.2",
        "scikit-image>=0.18.3"
        "tk",
    ],

    python_requires=">=3.7",


)