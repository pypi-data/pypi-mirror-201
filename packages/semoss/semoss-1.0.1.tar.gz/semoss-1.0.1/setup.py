from setuptools import setuptools,find_packages
with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="semoss",                     # This is the name of the package
    version="1.0.1",
    packages=find_packages(),
    install_requires=['pandas','requests'], 
    author="Thomas Trankle",                     # Full name of the author
    description="Utility package to connect to SEMOSS instances and query data",
    license="MIT",
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)