#!/bin/bash

set -u
set -e

# download spec
curl -fsSLo /root/rpmbuild/SPECS/$SPEC.spec https://raw.githubusercontent.com/softvisio/rpm/main/$SPEC.spec

# update packages
dnf -y update
dnf -y remove --oldinstallonly || true

# install spec deps
dnf -y builddep /root/rpmbuild/SPECS/$SPEC.spec

# build rpm
# --define='%_rpmfilename %{NAME}-%{EPOCH}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm' \
rpmbuild \
    -ba \
    /root/rpmbuild/SPECS/$SPEC.spec

ARCH=$(rpm -E %{?_build_arch})
REPO=/root/rpmbuild/build/repo/$(rpm -E %{?dist})-$ARCH

mkdir -p $REPO

# copy rpm
\cp /root/rpmbuild/RPMS/*/*.* $REPO

# refresh repodata
printf "\nCreating repo\n"
createrepo --update --database $REPO
