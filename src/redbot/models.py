from rich.table import Table
from rich.console import Console
from rich.align import Align
from rich import box

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


class Comment:
    def __init__(self, json_data):
        pass


class Issue:
    def __init__(self, issue):
        self.key = issue.id
        self.summary = issue.subject
        self.description = issue.description
        self.creator = issue.author
        self.assignee = getattr(issue, 'assigned_to', None)
        self.status = issue.status
        self.created = issue.created_on

    def _get_table_data(self):
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

                output.append(
                    [f'{data_key.title()}:', data]
                )

        return output

    def print(self, borders=True):
        print_table(self._get_table_data(), borders=borders)


def wrap_text(text):
    if text:
        return '\n'.join([line
                          for line in text.splitlines()])
    return ''


def print_key_summary(rows,
                      text_wrap=True,
                      borders=True):
    data = [
        (row[0], row[1])
        for row in rows]
    print_table(data,
                inner_heading_row_border=False,
                borders=borders)
