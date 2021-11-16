# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          repo-google-chrome
Version:       2
Release:       1%{?dist}
Epoch:         1
License:       GPL
URL:           https://chrome.google.com/
Summary:       Official Google Chrome repository
Group:         Development/Environment
Provides:      %{name} = %{epoch}:%{version}-%{release}
Requires:      gnu-free-sans-fonts

# {{{ description
%description
The official Google Chrome repository.
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d
cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/yum.repos.d/google-chrome.repo
[google-chrome]
name          = Google Chrome
baseurl       = https://dl.google.com/linux/chrome/rpm/stable/\$basearch
enabled       = 1
gpgcheck      = 1
repo_gpgcheck = 0
gpgkey        = https://dl.google.com/linux/linux_signing_key.pub
EOF
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/google-chrome.repo
# }}}
