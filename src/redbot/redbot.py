import argparse
import requests
from redbot.client import get_issue, get_assignee_issues, get_summary_issues
from redbot.models import print_key_summary


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
    cmd.add_argument(
        '--include-closed',
        action='store_true',
        help='Include issues with closed status')
    cmd.add_argument(
        '--max-results',
        dest='max_results',
        type=int,
        help='Maximum number of results to return')


def main():
    try:
        args = parser.parse_args()

        if args.subcommand_name in ('issue', 'issues'):
            if args.issue_keys:
                issue_keys = args.issue_keys
                for line_or_key in issue_keys:
                    for key in line_or_key.split():
                        try:
                            issue = get_issue(key)
                        except requests.exceptions.HTTPError:
                            print(f'Issue {key} was not found')
                            continue
                        issue.print(text_wrap=not args.quiet,
                                    borders=not args.quiet)
            else:
                rows = get_summary_issues(max_results=args.max_results)
                print_key_summary(rows,
                                  text_wrap=not args.quiet,
                                  borders=not args.quiet)
        elif args.subcommand_name in ('assignee',):
            if args.assignee:
                rows = []
                for assignee in args.assignee:
                    rows.extend(get_assignee_issues(assignee=assignee,
                                                    include_closed=args.include_closed,
                                                    max_results=args.max_results))
            else:
                rows = get_assignee_issues(include_closed=args.include_closed,
                                           max_results=args.max_results)
            print_key_summary(rows,
                              text_wrap=not args.quiet,
                              borders=not args.quiet)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
