import urllib.request
from urllib.error import URLError, HTTPError
import ssl
import json
from json import JSONDecodeError
import sys
import yaml

def count_pull_requests(accountName, project, repositoryId, date):
    limit = -1 # -1 means return all
    status = 'completed'
    url = 'https://{}.visualstudio.com/{}/_apis/git/repositories/{}/pullrequests?api-version=4.1&$top={}&searchCriteria.status={}'.format(
        accountName, project, repositoryId, limit, status
    )

    with open('cookie.txt') as cookie_file:
        cookie = cookie_file.read()

    headers = {'Cookie' : cookie}

    req = urllib.request.Request(url, None, headers)
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    try:
        response = urllib.request.urlopen(req, context=sslContext)
    except HTTPError as error:
        print('Error while getting response from VSTS. Error code: ', error.code, error.reason)
        sys.exit(2)
    except URLError as error:
        print('Error: ', error.reason)
        sys.exit(2)

    html = response.read()

    try:
        json_response = json.loads(html.decode('utf-8'))
    except JSONDecodeError as error:
        print("Error decoding json response: ", error)
        sys.exit(2)

    count = 0

    try:
        for item in json_response['value']:
            if item['status'] == status and item['closedDate'].startswith(date):
                count += 1
    except KeyError as error:
        print("Invalid json response: {} not found".format(error))
        sys.exit(2)

    if count == limit:
        print('WARNING! You need to increase limit, some PRs might not have been counted')

    return count

def main(argv):
    date = str(sys.argv[1])
    print('*** PULL REQUEST REPORT {} ***\n'.format(date))

    total_count = 0

    try:
        config = yaml.safe_load(open('config.yml'))
    except FileNotFoundError:
        print("You need to provide a config.yml file. Please see README for details.")
        sys.exit(2)

    try:
        for account in config:
            for project in config[account]:
                for repository_id in config[account][project].split():
                    count = count_pull_requests(account, project, repository_id, date)
                    print('{} PRs completed in {}'.format(count, repository_id))
                    total_count += count
    except TypeError:
        print("Invalid config.yml file. Please see README for details.")
        sys.exit(2)
    except AttributeError:
        print("Invalid config.yml file (You didn't provide any repositories). Please see README for details.")
        sys.exit(2)

    print('\n***************\n')
    print('{} PRs completed in total!'.format(total_count))

if __name__ == "__main__":
    main(sys.argv[1:])
