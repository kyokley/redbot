import os

from pathlib import Path
from redminelib import Redmine

_key_path_str = os.environ['KEY_PATH']
_key_path = Path(_key_path_str)

if not _key_path.exists():
    raise Exception(f'Could not find key at {_key_path}')

with open(_key_path) as f:
    _key = f.read().strip()

client = Redmine('http://redmine.ccbn.net/',
                 key=_key)
