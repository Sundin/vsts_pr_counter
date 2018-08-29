import urllib.request
import certifi
import json
import sys
import getopt
import yaml

def count_pull_requests(accountName, project, repositoryId, date):
    limit = 100
    status = 'completed'
    url ='https://{}.visualstudio.com/{}/_apis/git/repositories/{}/pullrequests?api-version=4.1&$top={}&searchCriteria.status={}'.format(accountName, project, repositoryId, limit, status)

    with open('cookie.txt') as f:
        cookie = f.read()

    headers = { 'Cookie' : cookie }

    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req, cafile=certifi.where())
    html = response.read()

    jsonResponse = json.loads(html.decode('utf-8'))

    count = 0

    for item in jsonResponse['value']:
        if item['status'] == status and item['closedDate'].startswith(date):
            count += 1

    if count == limit:
        print('WARNING! You need to increase limit, some PRs might not have been counted')

    return count

def main(argv):
    date = str(sys.argv[1])
    print('*** PULL REQUEST REPORT {} ***\n'.format(date))

    totalCount = 0

    config = yaml.safe_load(open('config.yml'))
    for account in config:
        for project in config[account]:
            for repositoryId in config[account][project].split():
                count = count_pull_requests(account, project, repositoryId, date)
                print('{} PRs completed in {}'.format(count, repositoryId))
                totalCount += count

    print('\n***************\n')
    print('{} PRs completed in total!'.format(totalCount))

if __name__ == "__main__":
   main(sys.argv[1:])
