# https://trac.ffmpeg.org/wiki/CompilationGuide/Centos

%define version %(git ls-remote --tags https://git.ffmpeg.org/ffmpeg.git | perl -lne 'm[refs/tags/n([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          ffmpeg
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       LGPL version 2.1 or later
URL:           https://ffmpeg.org
Summary:       FFmpeg is the leading multimedia framework
Group:         Development/Libraries
Source0:       https://ffmpeg.org/releases/ffmpeg-%{version}.tar.gz
BuildRequires: gcc make freetype-devel yasm nasm

# {{{ description
%description
FFmpeg is the leading multimedia framework, able to decode, encode, transcode, mux, demux, stream, filter and play pretty much anything that humans and machines have created. It supports the most obscure ancient formats up to the cutting edge. No matter if they were designed by some standards committee, the community or a corporation. It is also highly portable: FFmpeg compiles, runs, and passes our testing infrastructure FATE across Linux, Mac OS X, Microsoft Windows, the BSDs, Solaris, etc. under a wide variety of build environments, machine architectures, and configurations.
# }}}

# {{{ prep
%prep
%setup
# }}}

# {{{ build
%build

EXTRA_BUILD_DIR=%{_builddir}/ffmpeg-%{version}/BUILD
PATH=$PATH:$EXTRA_BUILD_DIR/bin

./configure \
    --prefix=%{_prefix} \
    --libdir=/usr/lib64 \
    --extra-cflags="-I$EXTRA_BUILD_DIR/include" \
    --extra-ldflags="-L$EXTRA_BUILD_DIR/lib" \
    --extra-libs=-lpthread \
    --extra-libs=-lm \
    --enable-libfreetype \
    --enable-nonfree

make %{_smp_mflags}
# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT
# }}}

# {{{ files
%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*
# }}}

# {{{ package devel
%package devel
Summary:       FFmpeg development files
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}, pkgconfig

%description devel

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
# }}}
