#! /usr/bin/python
"""
Scan through a dump of google groups and locate those with one
member, where the member is not another group.
"""

import httplib2
import argparse
import pprint
import sys

import pickle
import os.path


def find_empty_groups(groupdir):
    for email in groupdir:
        group = groupdir[email]
        if group['members'] is None:
            print email, group['directMembersCount']


def find_single_user_groups(groupdir):
    for email in groupdir:
        group = groupdir[email]
        members = group['members']
        if members is not None:
            if group['directMembersCount'] == '1' and members[0]['type'] == 'USER':
                    print email, '->', members[0]['email']


def main(argv):

    # Declare command-line flags.
    # addHelp=False here because it's added downstream in the sample_init

    argparser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    argparser.add_argument(
        '-i',
        '--input',
        default='./group_dump.pickle',
        help='filename of group dump file'
        )
    argparser.add_argument(
        '-v',
        '--verbose',
        help='Verbose output',
        action='store_true')
    argparser.add_argument(
        'command',
        choices=['empty', 'single_user_member'],
        help='Action to be taken')
    flags = argparser.parse_args(argv[1:])

    with open(flags.input, 'rb') as f:
        group_dump = pickle.load(f)

    if flags.verbose:
        dumpdate = group_dump['dumpdate']
        print 'Group Dump Date (UTC):',\
              dumpdate.strftime("%A, %d %B %Y %I:%M%p")
    groupdir = group_dump['groupdir']

    if flags.command == 'empty':
        find_empty_groups(groupdir)
    elif flags.command == 'single_user_member':
        find_single_user_groups(groupdir)
    else:
        print 'invalid command'

    # pprint.pprint(groupdir)

if __name__ == '__main__':
    main(sys.argv)
