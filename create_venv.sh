#!/bin/bash

# this installs the virtualenv module
python3 -m pip install virtualenv
# this creates a virtual environment named "env"
python3 -m venv env
# this activates the created virtual environment
source env/bin/activate
# updates pip
pip install -U pip
# this installs the required python packages to the virtual environment
# pip install -r requirements.txt

echo created environment

# Install the potentially troubling libraries
pip install warcio
pip install bs4
pip install requests
pip install nltk
pip install heapq
pip install sklearn
pip install spacy
pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz#egg=en_core_web_sm
