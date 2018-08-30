# VSTS-PR-COUNTER
The purpose of this repository is to count the number of completed pull requests in or more VSTS projects on a given date.

## Requirements
Tested with Python 3.7.0.

## Setup
Install Python dependencies:  
`pip install -r requirements.txt`

## Usage
Log in to VSTS in your browser, open your browser's developer tools, and copy the value of the `Cookie` parameter from any request. Paste into a new file called `cookie.txt`.

Create an new file called `config.yml`. Inside you have to enter the `accountName`, `projectName` and `repositoryName` of all the repositories you are interested in. Use the following format:

```
accountName: 
  project1:
    repository1
    repository2
  project2:
    analyze-prognose
    routes
```

Run the program with this command:  
`python vsts-pr-counter.py 2018-08-28`  
(replace with the date you are interested, in format YYY-MM-DD).

## Usage using virtualenv
[Virtualenv](https://virtualenv.pypa.io/en/stable/) is a useful tool if you need to switch between different Python versions. It can be used to create an isolated Python environment for each of your projects.

Install virtualenv:  
`easy_install virtualenv`

Create a new virtualenv environment with the following command:  
`virtualenv ENV -p python3.7`

Activate the virtualenv environment:  
`source ENV/bin/activate`
