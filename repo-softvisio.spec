# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-softvisio
Version:       10
Release:       1%{?dist}
Epoch:         1
License:       GPL
URL:           https://github.com/softvisio/rpm
Summary:       Softvisio private RPM repo
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}

# {{{ description
%description
Softvisio private RPM repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d

DIST=%{dist}
DIST=${DIST//[0-9]/}

cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/softvisio.repo
[softvisio]
name                = Softvisio
baseurl             = https://media.githubusercontent.com/media/softvisio/rpm/main/repo/$DIST\$releasever-\$basearch/
enabled             = 1
type                = rpm-md
gpgcheck            = 0
repo_gpgcheck       = 0
enabled_metadata    = 1
module_hotfixes     = 1
skip_if_unavailable = 1
EOF

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/softvisio.repo

# }}}
