%define version %(git ls-remote --tags git://github.com/tokuhirom/plenv.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

# disable automated shebang mungling
%undefine __brp_mangle_shebangs

Name:          plenv
Version:       %{version}
Release:       1%{?dist}
Epoch:         2
License:       GPLv2+
URL:           https://github.com/tokuhirom/plenv
Summary:       Perl binary manager
Group:         Development/Languages
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/tokuhirom/plenv/archive/master.tar.gz
Source1:       https://raw.githubusercontent.com/miyagawa/cpanminus/master/cpanm
Source2:       https://raw.githubusercontent.com/skaji/cpm/master/cpm
BuildArch:     noarch
AutoReq:       no

# {{{ description
%description
Perl binary manager.
# }}}

# {{{ prep
%prep
# }}}

# {{{ build
%build
# }}}

# {{{ install
%install

# plenv root dir
export PLENV_ROOT=${RPM_BUILD_ROOT}%{_prefix}/plenv

# plenv
install -m 755 -d $PLENV_ROOT
tar -C $PLENV_ROOT --strip-components=1 -xf %{SOURCE0}

# perl-build
install -m 755 -d $PLENV_ROOT/plugins/perl-build
curl -fsSL https://github.com/tokuhirom/Perl-Build/archive/master.tar.gz | tar -C $PLENV_ROOT/plugins/perl-build --strip-components=1 -xzf -

# plenv-contrib
install -m 755 -d $PLENV_ROOT/plugins/plenv-contrib
curl -fsSL https://github.com/miyagawa/plenv-contrib/archive/master.tar.gz | tar -C $PLENV_ROOT/plugins/plenv-contrib --strip-components=1 -xzf -

# cpanm
install -m755 %{SOURCE1} $PLENV_ROOT/bin

# cpm
install -m755 %{SOURCE2} $PLENV_ROOT/bin

# install bootstrap script
install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/plenv.sh
#!/bin/sh

export PLENV_ROOT=%{_prefix}/plenv

[[ :\$PATH: == *":\$PLENV_ROOT/bin:"* ]] || PATH+=":\$PLENV_ROOT/bin"

[[ :\$PATH: == *":\$PLENV_ROOT/shims:"* ]] || eval "\$(plenv init -)"

# cpanm
export PERL_CPANM_OPT="--metacpan --from https://cpan.metacpan.org/"
export PERL_CPANM_HOME=/tmp/.cpanm

# test harness
export HARNESS_OPTIONS=c
export HARNESS_SUMMARY_COLOR_SUCCESS="bold green"
export HARNESS_SUMMARY_COLOR_FAIL="bold red"

# WARNING!!! not all perl distributions can pass tests in parallel mode
# export HARNESS_OPTIONS=c:j9
EOF

# }}}

# {{{ postun
%postun

# uninstall, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
if [ "$1" == "0" ]; then
    rm -rf %{_prefix}/plenv
fi
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/plenv
%{_sysconfdir}/profile.d/plenv.sh
# }}}
