# Google Group Audit Tools
This is the first, poorly documented step towards some utilities to manage Google Groups within a Apps for Business domain.

These might not have any utility for any domain other than the domain they were written for, but hopefully they can be of some use.


## Files
* dump_groups.py: Creates a dictionary of all groups in the domain, along with members, indexed by the group email. By default creates a pickle file containing the dictionary, for use in other scripts or utilties. Used to cache the group data while testing script logic.
* group_audit.py: Runs a command line specified audit of the groups and members.

## Prerequisites
Prior to use, the client_secrets.json file must be generated via the Google Developer Console. See https://developers.google.com/api-client-library/python/start/get_started for instructions.

## Usage
### dump_groups.py
```
$ dump_groups.py [-v] [-h] domain
```
where domain is the Google Apps domain to dump.

### group_audit.py
```
$ group_audit.py [-v] [-i INPUT] command
```
where
* -i is an optional flag defining the dump file produced by dump_groups.py
* -v Versbose output. Will print the date the dump file was created.
* command: audit to run. The current audits are:
  - empty: groups that have no members
  - single_user_member: groups that have only one member, where the member is not another group
