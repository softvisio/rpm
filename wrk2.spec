%define release %(echo $(date -u +"%Y%m%d%H%M%%S").$(git ls-remote git://github.com/giltene/wrk2.git HEAD | awk '{print substr($1,1,8);}'))

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          wrk2
Version:       1
Release:       %{release}%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://github.com/giltene/wrk2
Summary:       A constant throughput, correct latency recording variant of wrk
Group:         Applications/Editors
Provides:      wrk2 = %{epoch}:%{version}-%{release}
Source0:       https://github.com/giltene/wrk2/archive/master.tar.gz
BuildRequires: openssl-devel zlib-devel

# {{{ description
%description
A constant throughput, correct latency recording variant of wrk.
# }}}

# {{{ prep
%prep
%setup -n wrk2-master
# }}}

# {{{ build
%build
gmake %{_smp_mflags}
# }}}

# {{{ install
%install
export PREFIX=${RPM_BUILD_ROOT}%{_prefix}/local/bin

install -m 755 -d $PREFIX

cp wrk $PREFIX/wrk2
# }}}

# {{{ files
%files
%defattr(-,root,root,-)
%{_prefix}/local/bin/wrk2
# }}}
