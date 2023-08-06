import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Miniengine',
    version='1.0.0',
    author='Rafael Rayes',
    author_email='rafa@rayes.com.br',
    description='Engine for pygame',
    long_description='''
   # Miniengine

Miniengine is a simple physics simulation library built on top of Pygame. It allows users to simulate the motion of objects, calculate collisions, and visualize the results. The library includes the `MiniEngine` module for handling physics calculations, and the `Renderer` class for rendering and displaying the simulations.

## Installation

To install Miniengine, simply type `pip install Miniengine` into your terminal if you have pip installed.

## Dependencies

- Pygame

## Documentation

The documentation isn't complete yet. You can access it in Github. There are also examples.

''',
    long_description_content_type="text/markdown",
    url='https://github.com/rrayes3110/Mini-Engine',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
