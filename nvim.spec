%define version %(curl --silent https://api.github.com/repos/neovim/neovim/releases/tags/nightly | perl -lne 'm[NVIM\\s+v([\\d.]+)-dev\\+(\\d+)]sm ? print $1 . "." . $2 : next')

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

# disable automated shebang mungling
%undefine __brp_mangle_shebangs

Name:          nvim
Version:       %{version}
Release:       1%{?dist}
Epoch:         2
License:       GPLv2.1+
URL:           https://github.com/neovim/neovim
Summary:       Neovim nightly
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz
AutoReq:       no

# {{{ description
%description
Neovim nightly build.
# }}}

# {{{ prep
%prep
# }}}

# {{{ build
%build
# }}}

# {{{ check
%check
# }}}

# {{{ install
%install

install -m 755 -d ${RPM_BUILD_ROOT}%{_prefix}/local
tar -C ${RPM_BUILD_ROOT}%{_prefix}/local --strip-components=1 -xzf %{SOURCE0}
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/local/*
# }}}
