%define perl_version 5.34.0
%define release %(date -u +"%Y%m%d%H%M%%S")

# allow to download sources
%undefine _disable_source_fetch

# disable binary stripping
%global __os_install_post %{nil}

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

# disable /usr/lib/.build-id dir generation
%define _build_id_links none

Name:           perl-%{perl_version}
Version:        1
Release:        %{release}%{?dist}
Epoch:          1

License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:            https://www.perl.org/
Summary:        Practical Extraction and Report Language
Group:          Development/Languages
Provides:       %{name} = %{epoch}:%{version}-%{release}
Source0:        https://www.cpan.org/src/5.0/perl-%{perl_version}.tar.gz
Source1:        perl-pre-install.sh
Source2:        https://bitbucket.org/softvisio/pcore/raw/master/cpanfile
Source3:        perl-post-install.sh

Requires:       plenv

BuildRequires:  plenv

BuildRequires:  gcc make patch
BuildRequires:  redhat-rpm-config
BuildRequires:  groff-base libdb-devel tcsh zlib-devel bzip2-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  gdbm-devel

BuildRequires:  openssl openssl-devel
BuildRequires:  libdb-devel
BuildRequires:  ncurses-devel readline-devel
BuildRequires:  libidn2-devel
BuildRequires:  libmaxminddb-devel
BuildRequires:  libxml2-devel
BuildRequires:  libjpeg-devel libtiff-devel libpng-devel freetype-devel giflib-devel libwebp-devel

# For tests
BuildRequires:  procps rsyslog

AutoReq:        no
AutoProv:       no

# Adjust tests to gdbm-1.15, https://rt.perl.org/Public/Bug/Display.html?id=133295
# Patch1:         perl-5.29.0-Remove-ext-GDBM_File-t-fatal.t.patch

# {{{ description
%description
Perl interpreter with pre-installed packages
# }}}

# {{{ prep
%prep

%setup -n perl-%{perl_version}

# %patch1 -p1

# }}}

# {{{ build
%build

/bin/sh Configure -des \
    -Dusemorebits \
    -Duselargefiles \
    -Dprefix=%{_prefix}/plenv/versions/%{name} \
    -Duserelocatableinc \
    -Dman1dir=none -Dman3dir=none

make %{_smp_mflags}

make test

# }}}

# {{{ install
%install

source /etc/profile.d/plenv.sh

PERL_INSTALL_ROOT=%{_prefix}/plenv/versions/%{name}
PERL_BUILD_ROOT=${RPM_BUILD_ROOT}${PERL_INSTALL_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT

# remove man, to avoid "unpackaged files" error
rm -f $RPM_BUILD_ROOT/*.0

PATH=$PERL_BUILD_ROOT/bin:$PATH

# relocate perl
find $PERL_BUILD_ROOT -type f -exec sed -i "s|$PERL_INSTALL_ROOT|$PERL_BUILD_ROOT|g" {} +

# run pre-install script
/bin/bash %{SOURCE1}

# install cpan-outdated
cpanm App::cpanoutdated

# update perl packages
cpan-outdated | cpanm

# install Pcore dependencies
cpanm --with-feature linux --with-recommends --with-suggests --with-develop --installdeps / --cpanfile %{SOURCE2}

# run post-install script
/bin/bash %{SOURCE3}

# relocate perl
find $PERL_BUILD_ROOT -type f -exec sed -i "s|$PERL_BUILD_ROOT|$PERL_INSTALL_ROOT|g" {} +

# }}}

# {{{ post
%post

if [[ -x "$(command -v plenv)" ]]; then
    plenv rehash
elif [[ -f "/etc/profile.d/plenv.sh" ]]; then
    source "/etc/profile.d/plenv.sh"
    plenv rehash
fi

# }}}

# {{{ postun
%postun

# uninstall, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
if [ "$1" == "0" ]; then
    rm -rf %{_prefix}/plenv/versions/%{name}
fi

if [[ -x "$(command -v plenv)" ]]; then
    plenv rehash
elif [[ -f "/etc/profile.d/plenv.sh" ]]; then
    source "/etc/profile.d/plenv.sh"
    plenv rehash
fi

# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/plenv/versions/%{name}

# }}}
