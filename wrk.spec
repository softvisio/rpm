%define release %(echo $(date -u +"%Y%m%d%H%M%%S").$(git ls-remote git://github.com/wg/wrk.git HEAD | awk '{print substr($1,1,8);}'))

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          wrk
Version:       1
Release:       %{release}%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://github.com/wg/wrk
Summary:       Modern HTTP benchmarking tool
Group:         Applications/Editors
Provides:      wrk = %{epoch}:%{version}-%{release}
Source0:       https://github.com/wg/wrk/archive/master.tar.gz
BuildRequires: openssl-devel

# {{{ description
%description
Modern HTTP benchmarking tool.
# }}}

# {{{ prep
%prep
%setup -n wrk-master
# }}}

# {{{ build
%build
gmake %{_smp_mflags}
# }}}

# {{{ install
%install
export PREFIX=${RPM_BUILD_ROOT}%{_prefix}/local/bin

install -m 755 -d $PREFIX

cp wrk $PREFIX
# }}}

# {{{ files
%files
%defattr(-,root,root,-)
%{_prefix}/local/bin/wrk
# }}}
