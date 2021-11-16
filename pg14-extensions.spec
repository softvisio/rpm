%define pg_version 14

%define timestamp %(if [ ! -f %{_sourcedir}/timestamp.txt ]; then date -u +"%Y%m%d%H%M%%S" > %{_sourcedir}/timestamp.txt; fi; cat %{_sourcedir}/timestamp.txt)

%define timescaledb_version %(git ls-remote --tags git://github.com/timescale/timescaledb.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          pg%{pg_version}-extensions
Version:       1
Release:       %{timestamp}%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://
Summary:       Extensions for Postgres
Group:         System Environment/Daemons
Provides:      %{name} = %{epoch}:%{version}-%{release}
BuildRequires: postgresql%{pg_version}-devel
BuildRequires: gcc cmake make redhat-rpm-config openssl-devel

# timecaledb
BuildRequires: krb5-devel perl-IPC-Run

# {{{ description
%description
Various extensions for PostgreSQL.
# }}}

# {{{ prep
%prep

# pg_softvisio
rm -rf $RPM_BUILD_DIR/pg_softvisio
mkdir $RPM_BUILD_DIR/pg_softvisio
curl -fsSL https://github.com/softvisio/pg-softvisio/archive/latest.tar.gz | tar -C $RPM_BUILD_DIR/pg_softvisio --strip-components=1 -xzf -

# timescaledb
rm -rf $RPM_BUILD_DIR/timescaledb
mkdir $RPM_BUILD_DIR/timescaledb
curl -fsSL https://github.com/timescale/timescaledb/archive/%{timescaledb_version}.tar.gz | tar -C $RPM_BUILD_DIR/timescaledb --strip-components=1 -xzf -

# }}}

# {{{ build
%build

export PATH=/usr/pgsql-%{pg_version}/bin:$PATH

# timescaldb
pushd $RPM_BUILD_DIR/timescaledb
./bootstrap
cd build && gmake %{_smp_mflags} CLANG=clang
popd

# }}}

# {{{ install
%install

export PATH=/usr/pgsql-%{pg_version}/bin:$PATH

# pg_softvisio
pushd $RPM_BUILD_DIR/pg_softvisio
gmake install DESTDIR=$RPM_BUILD_ROOT USE_PGXS=1
popd

# timescaledb
pushd $RPM_BUILD_DIR/timescaledb/build
gmake install DESTDIR=$RPM_BUILD_ROOT
popd

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/pgsql-%{pg_version}
# }}}
