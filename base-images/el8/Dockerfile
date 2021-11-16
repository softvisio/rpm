FROM centos:8

LABEL maintainer="zdm"

USER root

ADD . /tmp/rpmbuild

WORKDIR /root/rpmbuild/SPECS

RUN \
    bash /tmp/rpmbuild/env-rpm.sh \
    rm -rf /tmp/rpmbuild

ENTRYPOINT [ "/bin/bash", "-l" ]
