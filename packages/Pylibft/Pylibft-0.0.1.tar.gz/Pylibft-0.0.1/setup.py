from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'You can find here some functions that can help you during the autamation in CTF/Pentest.'

# Setting up
setup(
    name="Pylibft",
    version=VERSION,
    author="Wiloti",
    author_email="contact@wiloti.fr",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['termcolor', 'typing_extensions'],
    keywords=['python', 'CTF', 'Pentest', 'automation'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
