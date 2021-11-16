%define version 14.2

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          princexml
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       GPLv2.1+
URL:           https://www.princexml.com
Summary:       Convert your HTML documents to PDF
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://www.princexml.com/download/prince-%{version}-linux-generic-x86_64.tar.gz

# {{{ description
%description
Convert your HTML documents to PDF.
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

install -m 755 -d ${RPM_BUILD_ROOT}%{_prefix}/princexml
tar -C ${RPM_BUILD_ROOT}%{_prefix}/princexml --strip-components=3 -xf %{SOURCE0} prince-%{version}-linux-generic-x86_64/lib/prince

install -m 755 -d ${RPM_BUILD_ROOT}%{_bindir}
cat <<EOF > ${RPM_BUILD_ROOT}%{_bindir}/princexml
#!/bin/sh

exec "%{_prefix}/princexml/bin/prince" --prefix="%{_prefix}/princexml" "\$@"
EOF

chmod +x ${RPM_BUILD_ROOT}%{_bindir}/princexml
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_bindir}/*
%{_prefix}/princexml/*
# }}}
