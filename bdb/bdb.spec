%define version 18.1.40

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          bdb
Version:       %{version}
Release:       2%{?dist}
Epoch:         1
License:       BSD and LGPLv2 and Sleepycat
URL:           http://www.oracle.com/database/berkeley-db/
Summary:       Oracle Berkeley DB
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
# Source0:       https://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source0:       db-%{version}.tar.gz
BuildRequires: openssl-devel

# {{{ description
%description
Berkeley DB is a family of embedded key-value database libraries providing scalable high-performance data management services to applications. The Berkeley DB products use simple function-call APIs for data access and management.
# }}}

# {{{ prep
%prep

%setup -n db-%{version}
# }}}

# {{{ build
%build

cd build_unix

../dist/configure --prefix=%{_prefix}/local/%{name}

make %{_smp_mflags}
# }}}

# {{{ install
%install

cd build_unix

# TODO dbd-sql, gsg_db_server folders are missed in docs, this leads to the make install failure
make install DESTDIR=$RPM_BUILD_ROOT || true

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d

echo "%{_prefix}/local/%{name}/lib" > ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d/%{name}.conf
# }}}

# {{{ post
%post -p /sbin/ldconfig
# }}}

# {{{ postun
%postun -p /sbin/ldconfig
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/local/%{name}
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
# }}}
