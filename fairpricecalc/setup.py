import os
from setuptools import setup, find_packages

app_dependencies = [
    "pandas>=1.3.2",
    "lxml>=4.6.5",
    "dicttoxml>=1.7.4",
]

setup(
    name='fairpricecalc',
    version="1.0.0",
    url="https://github.com/ilb.ru/stockvaluation",
    description="Сервис расчёта справедливой цены ЦБ",
    author="Kuznetsov Maxim",
    extras_require={"dev": {} },
    install_requires=app_dependencies,
    py_modules=[],
    entry_points={
        'console_scripts': [
            'stockvaluation = __main__:main',]}
)