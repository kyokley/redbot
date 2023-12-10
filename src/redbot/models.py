import os
import json

from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box

from redbot.client import client

DEFAULT_PROJECT_INDEX = 19


console = Console()


def print_table(data,
                title='RedMineBot',
                borders=True):
    table = Table(box=box.ROUNDED if borders else None)
    table.add_column()
    if borders:
        table.add_column(Align(title, align='center'))
    else:
        table.add_column()

    for row in data:
        table.add_row(*row)

    console.print(table)


def print_key_summary(rows, borders=True):
    data = [(row[0], row[1]) for row in rows]
    print_table(data,
                inner_heading_row_border=False,
                borders=borders)


class User:
    USER_INDEX = os.environ.get('USER_INDEX')

    def __init__(self, user):
        self.key = str(user.id)
        self.name = f'{user.firstname} {user.lastname}'
        self._redmine_obj = user
        self._issues = None

    @classmethod
    def get(cls, key=None):
        key = key or cls.USER_INDEX
        if not key:
            raise Exception('USER_INDEX has not been defined')

        user = client.user.get(key)
        return cls(user)

    @property
    def issues(self):
        if self._issues is None:
            self._issues = [Issue(issue)
                            for issue in self._redmine_obj.issues]
        return self._issues


class Issue:
    def __init__(self, issue):
        self.key = str(issue.id)
        self.summary = issue.subject
        self.description = issue.description
        self.creator = issue.author
        self.assignee = getattr(issue, 'assigned_to', None)
        self.status = issue.status
        self.created = issue.created_on.isoformat()
        self._redmine_obj = issue

    @classmethod
    def get(cls, key):
        issue = client.issue.get(key)
        return cls(issue)

    def _get_table_data(self):
        output = []
        for data_key in ('key',
                         'summary',
                         'status',
                         'assignee',
                         'creator',
                         'description',
                         ):
            data = None
            if hasattr(self, data_key):
                if data_key in ('status',
                                'assignee',
                                'creator',
                                ):
                    attr = getattr(self, data_key)
                    data = attr.name if attr is not None else ''
                elif data_key in ('labels',):
                    data = ' '.join(getattr(self, data_key))
                else:
                    data = getattr(self, data_key)

                output.append(
                    [f'{data_key.title()}:', data]
                )

        return output

    def print(self, full=True):
        if full:
            print_table(self._get_table_data(), borders=full)
        else:
            print(f'{self.key:<7} {self.summary}')

    def to_dict(self):
        return {
            'key': self.key,
            'summary': self.summary,
            'description': self.description,
            'creator': self.creator,
            'assignee': self.assignee,
            'status': self.status,
            'created': self.created
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Project:
    PROJECT_INDEX = os.environ.get('PROJECT_INDEX') or DEFAULT_PROJECT_INDEX

    def __init__(self, project):
        self.name = project.name
        self.key = project.id
        self._redmine_obj = project
        self._issues = None

    @property
    def issues(self):
        if self._issues is None:
            self._issues = [Issue(issue)
                            for issue in self._redmine_obj.issues]
        return self._issues

    @classmethod
    def get(cls):
        project = client.project.get(cls.PROJECT_INDEX)
        return cls(project)
