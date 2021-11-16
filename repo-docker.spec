# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-docker
Version:       5
Release:       1%{?dist}
Epoch:         1
License:       GPL
URL:           https://get.docker.com/
Summary:       Official latest docker-ce repository
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}

# {{{ description
%description
The official latest docker-ce repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d

# fedora
%if 0%{?fedora}

    cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/docker.repo
[docker-ce-stable]
name          = Docker CE Stable
baseurl       = https://download.docker.com/linux/fedora/\$releasever/\$basearch/stable
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.docker.com/linux/fedora/gpg
EOF

# centos
%else

    cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/docker.repo
[docker-ce-stable]
name          = Docker CE Stable
baseurl       = https://download.docker.com/linux/centos/\$releasever/\$basearch/stable
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://download.docker.com/linux/centos/gpg
EOF

%endif

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/docker.repo
# }}}
