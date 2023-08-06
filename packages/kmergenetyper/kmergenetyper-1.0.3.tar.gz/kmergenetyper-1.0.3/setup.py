from setuptools import setup, find_packages

setup(
    name='kmergenetyper',
    version='1.0.3',
    packages=find_packages(),
    data_files=[],
    include_package_data=True,
    url='https://https://github.com/MBHallgren/kmergenetyper',
    license='',
    install_requires=(),
    author='Malte B. Hallgren',
    scripts=['bin/kmergenetyper'],
    author_email='malhal@food.dtu.dk',
    description='kmergenetyper - K-mer Gene Typer',
)