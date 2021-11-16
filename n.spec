%define version %(git ls-remote --tags git://github.com/tj/n.git | perl -lne 'm[refs/tags/v([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

# disable automated shebang mungling
%undefine __brp_mangle_shebangs

Name:          n
Version:       %{version}
Release:       1%{?dist}
Epoch:         3
License:       GPLv2+
URL:           https://github.com/tj/n
Summary:       Node version management
Group:         Development/Languages
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/tj/n/archive/master.tar.gz
BuildArch:     noarch
AutoReq:       no

# {{{ description
%description
Node version management.
# }}}

# {{{ prep
%prep
# }}}

# {{{ build
%build
# }}}

# {{{ install
%install

# n root dir
export N_PREFIX=${RPM_BUILD_ROOT}%{_prefix}/n

# n
install -m 755 -d $N_PREFIX
tar -C $N_PREFIX --strip-components=1 -xf %{SOURCE0}

# install bootstrap script
install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/n.sh
#!/bin/sh

export N_PREFIX=%{_prefix}/n

NPM_PREFIX=\$(realpath ~)/.npm/bin

[[ :\$PATH: == *":\$NPM_PREFIX:"* ]] || PATH+=":\$NPM_PREFIX"

[[ :\$PATH: == *":\$N_PREFIX/bin:"* ]] || PATH+=":\$N_PREFIX/bin"
EOF

# }}}

# {{{ postun
%postun

# uninstall, https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
if [ "$1" == "0" ]; then
    rm -rf %{_prefix}/n
fi
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/n
%{_sysconfdir}/profile.d/n.sh
# }}}
