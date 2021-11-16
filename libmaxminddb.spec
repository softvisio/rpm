%define version %(git ls-remote --tags git://github.com/maxmind/libmaxminddb.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          libmaxminddb
Version:       %{version}
Release:       3%{?dist}
Epoch:         1
License:       ASL 2.0 and BSD
URL:           https://maxmind.github.io/libmaxminddb/
Summary:       Library for country/city/organization to IP address or hostname mapping
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/maxmind/libmaxminddb/releases/download/%{version}/libmaxminddb-%{version}.tar.gz
BuildRequires: perl

# {{{ description
%description
The package contains libmaxminddb library.
# }}}

# {{{ prep
%prep
%setup
# }}}

# {{{ build
%build
%configure

make %{_smp_mflags}

make check
# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT
# }}}

%ldconfig_scriptlets

# {{{ files
%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_prefix}/share/*
# }}}

# {{{ package devel
%package devel
Summary:       Libmaxminddb development files
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.la
# }}}
