# Google Group Audit Tools
This is the first, poorly document step towards some utilities to manage Google Groups within a Apps for Business domain.

## Files
* dump_groups.py: Creates a dictionary of all groups in the domain, along with members, indexed by the group email. By default creates a pickle file containing the dictionary, for use in other scripts or utilties.

## Prerequisites
Prior to use, the client_secrets.json file must be generated via the Google Developer Console. See https://developers.google.com/api-client-library/python/start/get_started for instructions. 
