# VSTS-PR-COUNTER
The purpose of this repository is to count the number of completed pull requests in a set of VSTS project on a given date.

## Requirements
Python 3.7.0

Install virtualenv: `easy_install virtualenv`

## Setup
Activate virtualenv environment: `source ENV/bin/activate`

Install Python dependencies: `pip install -r requirements.txt`

## Usage
Log in to VSTS in your browser, and copy paste the `Cookie` parameter from any request. Paste into a new file called `cookie.txt`.

`python vsts-pr-counter.py 2018-08-28` (input the date you are interested on format YYY-MM-DD)

## Notes
The virtualenv configuration was created with the following command: `virtualenv ENV -p python3.7`
