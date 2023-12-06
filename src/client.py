import requests
import os

from pathlib import Path

from src.auth import get_creds
from src.models import Issue
from src.templates import ISSUE_URL, SEARCH_URL, SUMMARY_URL

from redminelib import Redmine

BATCH_RESULTS = 1000
MAXIMUM_RESULTS = 1000

_key_path_str = os.environ['KEY_PATH']
_key_path = Path(_key_path_str)

if not _key_path.exists():
    raise Exception(f'Could not find key at {_key_path}')

with open(_key_path) as f:
    KEY = f.read().strip()

CLIENT = Redmine('http://redmine.ccbn.net/',
                 key=KEY)

def get_issue(issue_name):
    username, api_token = get_creds()
    url = ISSUE_URL.format(issue=issue_name)
    resp = requests.get(url, auth=(username, api_token))
    resp.raise_for_status()
    issue = Issue(resp.json())
    return issue


def get_assignee_issues(assignee=None,
                        include_closed=False,
                        max_results=None):
    if max_results is None:
        max_results = MAXIMUM_RESULTS

    username, api_token = get_creds()

    start_at = 0
    batch_results = BATCH_RESULTS

    params = {'startAt': start_at,
              'maxResults': batch_results}
    params['jql'] = ''

    if assignee is None:
        assignee = username.split('@')[0]

    if isinstance(assignee, list):
        params['jql'] = f'assignee in ({",".join(assignee)})'
    else:
        params['jql'] = f'assignee = {assignee}'

    if not include_closed:
        params['jql'] = (' and '.join(['status != closed',
                                      params['jql']])
                         if params['jql']
                         else 'status != closed')

    params['jql'] = f'{params["jql"]} order by createdDate desc'

    prepped_req = requests.PreparedRequest()
    prepped_req.prepare_url(SEARCH_URL, params)
    resp = requests.get(prepped_req.url, auth=(username, api_token))
    data = resp.json()
    total_results = data['total']

    for issue in data['issues'][:max_results]:
        yield issue['key'], issue['fields']['summary']

    start_at = start_at + batch_results

    num_results = min(max_results, total_results)

    while start_at < num_results:
        params['startAt'] = start_at
        prepped_req = requests.PreparedRequest()
        prepped_req.prepare_url(SEARCH_URL, params)
        resp = requests.get(prepped_req.url, auth=(username, api_token))
        data = resp.json()

        if start_at + len(data['issues']) > num_results:
            num_results_to_display = (start_at + len(data['issues'])) - num_results
        else:
            num_results_to_display = len(data['issues'])

        for issue in data['issues'][:num_results_to_display]:
            yield issue['key'], issue['fields']['summary']

        start_at = start_at + batch_results


def get_summary_issues(assignee=None,
                       include_closed=False,
                       max_results=None):
    if max_results is None:
        max_results = MAXIMUM_RESULTS

    username, api_token = get_creds()

    start_at = 0
    batch_results = BATCH_RESULTS

    params = {'startAt': start_at,
              'maxResults': batch_results}
    params['jql'] = ''

    if assignee is not None:
        params['jql'] = f'assignee = {assignee}'

    if not include_closed:
        params['jql'] = (' and '.join(['status != closed',
                                      params['jql']])
                         if params['jql']
                         else 'status != closed')

    params['jql'] = f'{params["jql"]} order by createdDate desc'

    prepped_req = requests.PreparedRequest()
    prepped_req.prepare_url(SUMMARY_URL, params)
    resp = requests.get(prepped_req.url, auth=(username, api_token))
    data = resp.json()
    total_results = data['total']
    batch_results = data['maxResults']
    for issue in data['issues'][:max_results]:
        yield issue['key'], issue['fields']['summary']

    start_at = start_at + batch_results

    num_results = min(max_results, total_results)

    while start_at < num_results:
        params['startAt'] = start_at
        params['maxResults'] = start_at + batch_results
        prepped_req = requests.PreparedRequest()
        prepped_req.prepare_url(SUMMARY_URL, params)
        resp = requests.get(prepped_req.url, auth=(username, api_token))
        data = resp.json()

        if start_at + len(data['issues']) > num_results:
            num_results_to_display = (start_at + len(data['issues'])) - num_results
        else:
            num_results_to_display = len(data['issues'])

        for issue in data['issues'][:num_results_to_display]:
            yield issue['key'], issue['fields']['summary']

        start_at = start_at + batch_results
        total_results = data['total']
