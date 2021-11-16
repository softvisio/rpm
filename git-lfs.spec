%define version %(git ls-remote --tags git://github.com/git-lfs/git-lfs.git | perl -lne 'm[refs/tags/v([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          git-lfs
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       GPLv2.1+
URL:           https://git-lfs.github.com
Summary:       Git extension for versioning large files
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/git-lfs/git-lfs/releases/download/v%{version}/git-lfs-linux-amd64-v%{version}.tar.gz
Requires:      git

# {{{ description
%description
Git extension for versioning large files.
# }}}

# {{{ prep
%prep
# }}}

# {{{ build
%build
# }}}

# {{{ check
%check
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_prefix}/local/bin

tar -C ${RPM_BUILD_ROOT}%{_prefix}/local/bin -xf %{SOURCE0} git-lfs
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/local/bin/git-lfs
# }}}
