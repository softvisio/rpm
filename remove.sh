#!/bin/bash

set -u
set -e

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch $1" --prune-empty --tag-name-filter cat -- --all

createrepo --update --database $(dirname "$1")
