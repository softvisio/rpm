%define version %(git ls-remote --tags git://github.com/DanBloomberg/leptonica.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          leptonica
Version:       %{version}
Release:       3%{?dist}
Epoch:         1
License:       ASL 2.0 and BSD
URL:           https://github.com/danbloomberg/leptonica
Summary:       C library for efficient image processing and image analysis operations
Group:         Development/Libraries
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/DanBloomberg/leptonica/releases/download/%{version}/leptonica-%{version}.tar.gz
BuildRequires: gcc automake autoconf libtool
BuildRequires: giflib-devel libjpeg-devel openjpeg2-devel libpng-devel libtiff-devel libwebp-devel zlib-devel

# {{{ description
%description
The library supports many operations that are useful on
    * Document images
    * Natural images

Fundamental image processing and image analysis operations
    * Rasterop (aka bitblt)
    * Affine transforms (scaling, translation, rotation, shear) on images of arbitrary pixel depth
    * Projective and bi-linear transforms
    * Binary and gray scale morphology, rank order filters, and convolution
    * Seed-fill and connected components
    * Image transformations with changes in pixel depth, both at the same scale and with scale change
    * Pixelwise masking, blending, enhancement, arithmetic ops, etc.
# }}}

# {{{ prep
%prep
%setup
# }}}

# {{{ build
%build
%configure

make %{_smp_mflags}
# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT
# }}}

%ldconfig_scriptlets

# {{{ files
%files
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.so.*
# }}}

# {{{ package devel
%package devel
Summary:       Leptonica development files
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/cmake/LeptonicaConfig-version.cmake
%{_libdir}/cmake/LeptonicaConfig.cmake
# }}}

# {{{ package tools
%package tools
Summary:       Leptonica utility tools
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools

%files tools
%defattr(-,root,root,-)
%{_bindir}/*
# }}}
