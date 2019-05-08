import os
from setuptools import setup, find_packages

import app

setup(
    name='fairpricecalc',
    entry_points={
        'console_scripts': [
            'stockvaluation = __main__:main',]}
)