#! /usr/bin/python
"""
Utility to dump all groups and their members from a Google Apps domain.
"""

from collections import defaultdict
import httplib2
import argparse
import pprint
import sys
import random
from retrying import retry
import time

from apiclient.errors import HttpError
from apiclient.http import BatchHttpRequest
from apiclient.http import HttpMock
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
# only needed for testing
import pickle
import os.path


def list_group_members(member_service, group_id):
    members = []
    request = member_service.list(groupKey=group_id)
    while (request is not None):
        response = execute_with_backoff(request)
        try:
            members.extend(response['members'])
        except KeyError:
            return None
        request = member_service.list_next(request, response)

    return members


def retrieve_all_groups(group_service, domain):
    all_groups = []
    request = group_service.list(domain=domain)
    while (request is not None):
        response = execute_with_backoff(request)
        all_groups.extend(response['groups'])
        request = group_service.list_next(request, response)
    return all_groups


def retry_if_http_error(exception):
    """Return True if we should retry  False otherwise"""
    return isinstance(exception, HttpError)


# Implment backoff in case of API rate errors
@retry(wait_exponential_multiplier=1000,
       wait_exponential_max=10000,
       retry_on_exception=retry_if_http_error,
       wrap_exception=False)
def execute_with_backoff(request):
    response = request.execute()
    return response


def main(argv):

    # Declare command-line flags.
    # addHelp=False here because it's added downstream in the sample_init
    argparser = argparse.ArgumentParser(add_help=False)

    argparser.add_argument(
        'domain',
        help='The domain to fetch groups and members from')
    argparser.add_argument(
        '-v',
        '--verbose',
        help='Show progress',
        action='store_true')

    # Authenticate and construct service
    scope = ("https://www.googleapis.com/auth/admin.directory.group"
             "admin.directory.group.member")
    service, flags = sample_tools.init(
        argv, 'admin', 'directory_v1', __doc__, __file__, parents=[argparser],
        scope=scope
        )

    exit
    group_service = service.groups()
    if flags.verbose:
        print 'Retrieving group list for', flags.domain
    all_groups = retrieve_all_groups(group_service, flags.domain)
    if flags.verbose:
        print len(all_groups), 'retrieved'
        print 'Retrieving member lists for groups'

# Convert the API return to a dictionary
    group_dump = {}
    member_service = service.members()
    for group in all_groups:
        group_dump[group['email']] = {
            'name': group['name'],
            'id': group['id'],
            'directMembersCount': group['directMembersCount'],
            'description': group['description']
        }
        if flags.verbose:
            print 'Fetching', \
                group['email'], \
                len(group_dump), \
                'of', \
                len(all_groups)
        members = list_group_members(member_service, group['id'])
        group_dump[group['email']]['members'] = members

    if flags.verbose:
        print 'All members retrieved. Dumping pickle file'

    with open('group_dump.pickle', 'wb') as f:
        pickle.dump(group_dump, f)

if __name__ == '__main__':
    main(sys.argv)
