# TODO autodetect latest MariaDB release
%define version 10.6

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-mariadb
Version:       %{version}
Release:       7%{?dist}
Epoch:         1
License:       GPL
URL:           https://downloads.mariadb.org/mariadb/repositories/
Summary:       Official latest stable MariaDB repository
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}

# {{{ description
%description
The official latest stable MariaDB repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d

%if 0%{?fedora}
    OSNAME=fedora
%else
    OSNAME=centos
%endif

cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/mariadb.repo
# MariaDB %{version} Fedora repository list
# https://downloads.mariadb.org/mariadb/repositories/
[mariadb]
name          = MariaDB %{version}
baseurl       = https://yum.mariadb.org/%{version}/$OSNAME\$releasever-amd64
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
EOF

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/mariadb.repo
# }}}
