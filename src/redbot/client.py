import requests
import os

from pathlib import Path

from redbot.models import Issue

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
    pass


def get_assignee_issues(assignee=None,
                        include_closed=False,
                        max_results=None):
    if max_results is None:
        max_results = MAXIMUM_RESULTS

    pass


def get_summary_issues(assignee=None,
                       include_closed=False,
                       max_results=None):
    if max_results is None:
        max_results = MAXIMUM_RESULTS

    pass
