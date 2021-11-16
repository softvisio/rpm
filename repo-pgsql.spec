# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-pgsql
Version:       14
Release:       2%{?dist}
Epoch:         3
License:       GPL
URL:           https://yum.postgresql.org/
Summary:       Official latest PostgreSQL repository
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}

# {{{ description
%description
The official latest PostgreSQL repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d

%if 0%{?fedora}
    PLATFORM=fedora/fedora

    cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/pgsql.repo
[pgdg-common]
name          = PostgreSQL common RPMs
baseurl       = https://download.postgresql.org/pub/repos/yum/common/$PLATFORM-\$releasever-\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG

[pgdg14]
name          = PostgreSQL 14
baseurl       = https://download.postgresql.org/pub/repos/yum/14/$PLATFORM-\$releasever-\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF

%else
    PLATFORM=redhat/rhel

    cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/pgsql.repo
[pgdg-centos8-sysupdates]
name          = PostgreSQL Supplementary ucommon RPMs for RHEL/CentOS
baseurl       = https://download.postgresql.org/pub/repos/yum/common/pgdg-centos8-sysupdates/$PLATFORM-\$releasever-\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG

[pgdg-common]
name          = PostgreSQL common RPMs
baseurl       = https://download.postgresql.org/pub/repos/yum/common/$PLATFORM-\$releasever-\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG

[pgdg14]
name          = PostgreSQL 14
baseurl       = https://download.postgresql.org/pub/repos/yum/14/$PLATFORM-\$releasever-\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF

%endif

# }}}

# {{{ post
%post

%if 0%{?rhel}
    dnf -qy module disable postgresql llvm-toolset rust-toolset
%endif

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/pgsql.repo
# }}}
