#!/bin/bash

set -u
set -e

curl -fsSL https://raw.githubusercontent.com/softvisio/scripts/main/env-build-rpm.sh | /bin/bash

dnf -y install createrepo gcc cmake make redhat-rpm-config clang llvm openssl-devel
