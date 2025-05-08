
from setuptools import setup, find_packages

setup(
    name="GameV1",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame"
    ],
    entry_points={
        'console_scripts': [
            'mein-spiel=GameV1.main:main',
        ],
    },
)
