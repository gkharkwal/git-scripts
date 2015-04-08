#/usr/bin/python
#
# Filename: noisy-checkout-listener.py
# Author  : Gaurav Kharkwal
# Email   : gaurav.kharkwal@gmail.com
# Date    : 20150407
#
# About:
#  This is a companion file for the git-noisy-checkout script.
#  It expects two arguments:
#   1. repository name
#   2. branch name
#  Given those, it updates its persistent cache of updated repos with their
#  checked out branches.

import sys
import os.path

REPO_MAP_PATH = os.path.dirname(__file__) + '/repo_branch_info.txt'

def load(fh):
    """
        Assumes:
          `fh` is a valid file handle to a file that contains data
          in the following form:
            <repo-name> : <branch-name>
    """
    repoMap = {}
    for line in fh.readlines():
        line = line.strip()
        if not line: continue

        # Make assumptions about data
        repo, branch = line.split(':')
        repoMap[repo.strip()] = branch.strip()
    return repoMap

def dump(repoMap, fh):
    """
        Assumes:
         (a) `repoMap` is a string to string dictionary that maps
             repo-names to branch-names.
         (b) `fh` is a valid write-allowed file handle
    """
    longestRepoNameLen = -1
    for repo, branch in repoMap.items():
        if len(repo) > longestRepoNameLen:
            longestRepoNameLen = len(repo)

    for repo, branch in sorted(repoMap.items()):
        repo += ' '*(longestRepoNameLen - len(repo))
        fh.write('{0}: {1}\n'.format(repo, branch))

def main():
    if len(sys.argv) != 3:
        print 'Usage: noisy-checkout-listener.py <repo-name> <branch-name>'
        sys.exit(-1);

    repo   = sys.argv[1].strip()
    branch = sys.argv[2].strip()

    repoMap = {}

    # If an old copy of the map already exists, load it
    if os.path.isfile(REPO_MAP_PATH):
        with open(REPO_MAP_PATH) as fh:
            repoMap = load(fh)

    # Update repository info with the provided branch name
    repoMap[repo] = branch

    # Save map to a local copy
    with open(REPO_MAP_PATH, 'w') as fh:
        dump(repoMap, fh)

if __name__ == '__main__':
    main()

