%define version %(git ls-remote --tags git://github.com/krallin/tini.git | perl -lne 'm[refs/tags/v([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          tini
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://github.com/krallin/tini/
Summary:       Tini is the simplest init you could think of
Group:         System Environment/Daemons
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/krallin/tini/archive/v%{version}.tar.gz
BuildRequires: cmake make glibc-static

# {{{ description
%description
Tini is the simplest init you could think of.
# }}}

# {{{ prep
%prep

%setup
# }}}

# {{{ build
%build
export CFLAGS="-DPR_SET_CHILD_SUBREAPER=36 -DPR_GET_CHILD_SUBREAPER=37"

cmake . 

make %{_smp_mflags}
# }}}

# {{{ install
%install

make install DESTDIR=$RPM_BUILD_ROOT
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/local/bin/*
# }}}
