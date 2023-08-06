from setuptools import setup, find_packages

setup(
    name='PyWare',
    version="0.0.2",
    description="Package for ease of access to game hacking",
    long_description=open("README.txt").read(),
    url='https://kiy.rip/',
    author='Geek',
    author_email='gaminggeekeh@gmail.com',
    keywords='',
    packages=find_packages(),
    install_requires=['pymem']
)
