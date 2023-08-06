from setuptools import find_packages, setup

setup(
    name='co2_AT_emission',
    packages=find_packages(include=['co2_AT_emission']),
    version='0.1.1',
    description='My first python library',
    author='Raziuddin Khazi',
    author_email='raziuddin.khazi@alexanderthamm.com',
    install_requires=['pytz==2021.3', 'eco2ai==0.3.8'],
)
