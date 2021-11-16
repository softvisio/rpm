%define sourceforge_mirror iweb

# allow to download sources
%undefine _disable_source_fetch

Name:          msttcorefonts
Version:       2.5
Release:       1%{?dist}
Epoch:         1
License:       Spec file is GPL, binary rpm is gratis but non-distributable
URL:           http://corefonts.sourceforge.net/
Summary:       TrueType core fonts for the web
Group:         User Interface/X
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/andale32.exe
Source1:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/arial32.exe
Source2:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/arialb32.exe
Source3:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/comic32.exe
Source4:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/courie32.exe
Source5:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/georgi32.exe
Source6:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/impact32.exe
Source7:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/times32.exe
Source8:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/trebuc32.exe
Source9:       https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/webdin32.exe
Source10:      https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/verdan32.exe
Source11:      https://%{sourceforge_mirror}.dl.sourceforge.net/project/corefonts/the%20fonts/final/wd97vwr32.exe
BuildArch:     noarch
BuildRequires: ttmkfdir
# TODO uncomment, when cabextract for el8 will be available
# BuildRequires: cabextract

# {{{ description
%description
The TrueType core fonts for the web that was once available from
http://www.microsoft.com/typography/fontpack/. The src rpm is cleverly
constructed so that the actual fonts are downloaded from Sourceforge's site
at build time. Therefore this package technically does not 'redistribute'
the fonts, it just makes it easy to install them on a linux system.
# }}}

# {{{ prep
%prep

# TODO remove, when cabextract for el8 will be available
dnf -y install https://www.cabextract.org.uk/cabextract-1.9.1-1.i386.rpm
# }}}

# {{{ build
%build

cabextract --lowercase %{SOURCE0}
cabextract --lowercase %{SOURCE1}
cabextract --lowercase %{SOURCE2}
cabextract --lowercase %{SOURCE3}
cabextract --lowercase %{SOURCE4}
cabextract --lowercase %{SOURCE5}
cabextract --lowercase %{SOURCE6}
cabextract --lowercase %{SOURCE7}
cabextract --lowercase %{SOURCE8}
cabextract --lowercase %{SOURCE9}
cabextract --lowercase %{SOURCE10}
cabextract --lowercase %{SOURCE11}
# }}}

# {{{ install
%install

install -m755 -d $RPM_BUILD_ROOT/usr/share/fonts/%{name}

cp *.ttf $RPM_BUILD_ROOT/usr/share/fonts/%{name}

ttmkfdir --font-dir=$RPM_BUILD_ROOT/usr/share/fonts/%{name} --output=$RPM_BUILD_ROOT/usr/share/fonts/%{name}/fonts.dir

# }}}

# {{{ post
%post

if [ -x /usr/sbin/chkfontpath -a $1 -eq 1 ]; then
    /usr/sbin/chkfontpath --add /usr/share/fonts/%{name}
fi

if [ -x /usr/bin/fc-cache ]; then
    /usr/bin/fc-cache
fi
# }}}

# {{{ preun
%preun

if [ -x /usr/sbin/chkfontpath -a $1 -eq 0 ]; then
    /usr/sbin/chkfontpath --remove /usr/share/fonts/%{name}
fi
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
/usr/share/fonts/%{name}/*
# }}}
