%define version %(git ls-remote --tags https://gitlab.com/libidn/libidn2.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          libidn2
Version:       %{version}
Release:       5%{?dist}
Epoch:         4
License:       (GPLv2+ or LGPLv3+) and GPLv3+
URL:           https://www.gnu.org/software/libidn/#libidn2
Summary:       Library to support IDNA2008 internationalized domain names
Group:         Development/Libraries
Provides:      bundled(gnulib)
Provides:      libidn2.so.0()(64bit)
Provides:      libidn2.so.0(IDN2_0.0.0)(64bit)
Source0:       https://ftp.gnu.org/gnu/libidn/libidn2-%{version}.tar.gz
BuildRequires: gettext
# BuildRequires: libunistring-devel

# {{{ description
%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC 5890, 5891, 5892, 5893 and TR46 for internationalized domain names (IDN). It is a standalone library, without any dependency on libidn.
# }}}

# {{{ prep
%prep
%setup
# }}}

# {{{ build
%build

%configure CFLAGS="-fPIC"

make %{_smp_mflags}

# }}}

# {{{ check
%check
make %{_smp_mflags} -C tests check

# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_prefix}/share/info/dir

# pushd $RPM_BUILD_ROOT%{_libdir}
# %{__ln_s} -f libidn2.so.4.0.0 libidn2.so.0
# popd

# }}}

%ldconfig_scriptlets

# {{{ files
%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_prefix}/share/*

# }}}

# {{{ package devel
%package devel
Summary:       Libidn2 development files
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}, pkgconfig

%description devel

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

# }}}
