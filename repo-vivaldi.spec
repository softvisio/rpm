# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-vivaldi
Version:       1
Release:       1%{?dist}
Epoch:         1
License:       GPL
URL:           https://vivaldi.com/
Summary:       Official Vivaldi repository
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}
Requires:      gnu-free-sans-fonts

# {{{ description
%description
The official Vivaldi repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d
cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/vivaldi.repo
[vivaldi]
name          = Vivaldi
baseurl       = https://repo.vivaldi.com/archive/rpm/\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://repo.vivaldi.com/archive/linux_signing_key.pub
EOF
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/vivaldi.repo
# }}}
