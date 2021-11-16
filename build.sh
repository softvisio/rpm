#!/bin/bash

set -u
set -e

function _build_rpm() {
    local SCRIPT_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

    docker run \
        -e SPEC="$1" \
        --rm -it --shm-size=1g \
        -v $SCRIPT_DIR:/root/rpmbuild/build \
        --entrypoint /root/rpmbuild/build/build/build-rpm.sh \
        "softvisio/rpm:$2"

    printf "\nCommitting updates\n"
    git add .
    git commit -m"chore: rpm build $1:$2" -a

    printf "\nPushing updates\n"
    git push
}

if [ $# -eq 1 ]; then
    _build_rpm "$1" el8
    _build_rpm "$1" fc35
elif [ $# -eq 2 ]; then
    _build_rpm "$1" "$2"
else
    echo Invalid number of arguments

    exit 1
fi
