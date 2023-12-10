import argparse
from redbot.models import User, Issue, Project


parser = argparse.ArgumentParser(description='RedMine CLI')
subcommands = parser.add_subparsers(dest='subcommand_name')

issue_cmd = subcommands.add_parser(
    'issue',
    description='Pull information for a specific issue',
)
issues_cmd = subcommands.add_parser(
    'issues',
    description='Alias for the issue command',
)

for cmd in (issue_cmd, issues_cmd):
    cmd.add_argument(
        'issue_keys',
        metavar='key',
        nargs='*',
        help='issue keys',
    )

assignee_cmd = subcommands.add_parser(
    'assignee',
    description='Get issues for a specific user',
)
assignee_cmd.add_argument(
    'assignee',
    nargs='*',
    help='Assignee(s) to filter results by'
)

ALL_CMDS = (issue_cmd, issues_cmd, assignee_cmd)
for cmd in ALL_CMDS:
    cmd.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Display output without table formatting or text wrapping.')


def main():
    try:
        args = parser.parse_args()

        if args.subcommand_name in ('issue', 'issues'):
            if args.issue_keys:
                issue_keys = args.issue_keys
                for line_or_key in issue_keys:
                    for key in line_or_key.split():
                        try:
                            issue = Issue.get(key)
                        except Exception as e:
                            print(f'Error getting Issue={key} was not found')
                            print(e)
                            continue
                        issue.print(full=not args.quiet)
            else:
                project = Project.get()
                for issue in project.issues:
                    issue.print(full=not args.quiet)
        elif args.subcommand_name in ('assignee',):
            if args.assignee:
                indices = args.assignee
            else:
                indices = [User.USER_INDEX]

            for assignee in indices:
                user = User.get(assignee)
                for issue in user.issues:
                    issue.print(full=not args.quiet)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
