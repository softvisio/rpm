#!/bin/bash

set -u
set -e

SCRIPT_DIR="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

function _build_base_image() {
    docker build \
        --tag softvisio/rpm:$1 \
        --file $1/Dockerfile \
        --pull \
        --no-cache \
        --shm-size=1g \
        $SCRIPT_DIR

    docker push softvisio/rpm:$1
}

_build_base_image el8
_build_base_image fc35
