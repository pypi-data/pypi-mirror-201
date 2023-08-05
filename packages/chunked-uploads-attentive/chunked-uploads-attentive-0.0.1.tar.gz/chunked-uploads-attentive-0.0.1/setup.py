from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Chunked Upload of files on gcs using Django'
LONG_DESCRIPTION = 'A package that allows to transfer files and resume in case of data failure'

# Setting up
setup(
    name="chunked-uploads-attentive",
    version=VERSION,
    author="Ayion",
    author_email="<ayan@attentive.ai>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['django', 'djangorestframework'],
    keywords=['python', 'file', 'transfer', 'chunk', 'chunks', 'upload'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)