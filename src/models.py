from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box

import dateutil.parser

console = Console()


def print_table(data,
                title='RedMineBot',
                borders=True):
    table = Table(box=box.ROUNDED if borders else None)
    table.add_column()
    table.add_column(Align(title, align='center'))

    for row in data:
        table.add_row(*row)

    console.print(table)


class Status:
    def __init__(self, json_data):
        self.description = json_data['description']
        self.name = json_data['name']


class User:
    def __init__(self, json_data):
        self.name = json_data.get('displayName', 'None') if json_data else 'None'
        self.email = json_data.get('emailAddress', 'None') if json_data else 'None'


class Comment:
    def __init__(self, json_data):
        pass


class Issue:
    def __init__(self, json_data):
        self.key = json_data['key']
        self.summary = json_data['fields']['summary']
        self.description = json_data['fields']['description']
        self.creator = User(json_data['fields']['creator'])
        self.assignee = User(json_data['fields']['assignee'])
        self.labels = json_data['fields']['labels']
        self.status = Status(json_data['fields']['status'])
        self.created = dateutil.parser.parse(json_data['fields']['created'])
        self.updated = dateutil.parser.parse(json_data['fields']['updated'])
        self.link = BROWSER_LINK_TEMPLATE.format(issue_key=self.key)

        self.comments = [Comment(comment) for comment in json_data['fields']['comment']['comments']]

    def _get_table_data(self, text_wrap=True):
        if text_wrap:
            max_label_length = len('Description:') + 8
            wrap_width = min(term.width - max_label_length, 70)

        output = []
        for data_key in ('key',
                         'link',
                         'summary',
                         'status',
                         'labels',
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
                    data = attr.name
                elif data_key in ('labels',):
                    data = ' '.join(getattr(self, data_key))
                else:
                    data = getattr(self, data_key)

                if text_wrap:
                    data = wrap_text(data, width=wrap_width)

                output.append(
                    [f'{data_key.title()}:', data]
                )

        return output

    def print(self, text_wrap=True, borders=True):
        print_table(self._get_table_data(text_wrap=text_wrap), borders=borders)


def wrap_text(text, width=70):
    if text:
        return '\n'.join([textwrap.fill(line,
                                        width=width,
                                        replace_whitespace=False)
                          for line in text.splitlines()])
    return ''


def print_key_summary(rows,
                      text_wrap=True,
                      borders=True):
    max_label_length = len('ABC-XXXXX') + 8
    wrap_width = min(term.width - max_label_length, 70)
    if text_wrap:
        data = [
            (row[0], wrap_text(row[1], width=wrap_width))
            for row in rows]
    else:
        data = [
            (row[0], row[1])
            for row in rows]
    print_table(data,
                inner_heading_row_border=False,
                borders=borders)
