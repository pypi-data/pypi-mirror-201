from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.1.0'
DESCRIPTION = 'Flask Extension for multi language support.'

# Setting up
setup(
    name="flask-mulang",
    version=VERSION,
    author="Mohamed El-Hasnaouy",
    author_email="<elhasnaouymed@proton.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['flask', 'markdown', 'markupsafe'],
    keywords=['python', 'flask', 'language', 'babel', 'full stack', 'development'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
