%define version %(git ls-remote --tags git://github.com/z3APA3A/3proxy.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          3proxy
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://github.com/z3APA3A/3proxy
Summary:       3proxy tiny free proxy server
Group:         Applications/Editors
Provides:      3proxy = %{epoch}:%{version}-%{release}
Source0:       https://github.com/z3APA3A/3proxy/archive/%{version}.tar.gz

# {{{ description
%description
3Proxy tiny free proxy server is really tiny cross-platform (Win32/Win64&Unix) freeware proxy servers set. It includes HTTP proxy with HTTPS and FTP support, SOCKSv4/SOCKSv4.5/SOCKSv5 proxy (socks/socks.exe), POP3 proxy, SMTP proxy, AIM/ICQ proxy (icqpr/icqpr.exe), MSN messenger / Live messenger proxy (msnpr/msnpr.exe), FTP proxy, caching DNS proxy, TCP and UDP portmappers.
# }}}

# {{{ prep
%prep
%setup
# }}}

# {{{ build
%build
make %{_smp_mflags} -f Makefile.Linux
# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} -f Makefile.Linux
# }}}

# {{{ files
%files
%defattr(-,root,root,-)
/*
# % {_bindir}/*
# % {_prefix}/etc/*
# % {_mandir}/*/*
# }}}
