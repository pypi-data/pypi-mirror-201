from setuptools import setup

setup(
    # Application name:
    name='phonemeRecognizerWrapper',

    # Version number (initial):
    version='0.1.4',

    # Application author details:
    author='Petr Krýže',
    author_email='petr.kryze@gmail.com',

    # Packages
    packages=['phonemeRecognizerWrapper'],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url='https://github.com/PetrKryze/phonemeRecognizerWrapper',

    license='LICENSE.txt',

    description='Package containing one wrapper script over the Allosaurus phoneme recognition library, designed for '
                'passing the Allosaurus output data to MATLAB scripts for further analysis.',
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "allosaurus",
        "pydub",
        "setuptools"
    ],
)
