import urllib.request
import json
import sys
import yaml
import certifi

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
    response = urllib.request.urlopen(req, cafile=certifi.where())
    html = response.read()

    json_response = json.loads(html.decode('utf-8'))

    count = 0

    for item in json_response['value']:
        if item['status'] == status and item['closedDate'].startswith(date):
            count += 1

    if count == limit:
        print('WARNING! You need to increase limit, some PRs might not have been counted')

    return count

def main(argv):
    date = str(sys.argv[1])
    print('*** PULL REQUEST REPORT {} ***\n'.format(date))

    total_count = 0

    config = yaml.safe_load(open('config.yml'))
    for account in config:
        for project in config[account]:
            for repository_id in config[account][project].split():
                count = count_pull_requests(account, project, repository_id, date)
                print('{} PRs completed in {}'.format(count, repository_id))
                total_count += count

    print('\n***************\n')
    print('{} PRs completed in total!'.format(total_count))

if __name__ == "__main__":
    main(sys.argv[1:])
