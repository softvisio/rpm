%define version %(git ls-remote --tags git://github.com/tesseract-ocr/tesseract.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

%define tessdata_version %(git ls-remote --tags git://github.com/tesseract-ocr/tessdata.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:           tesseract
Version:        %{version}
Release:        3%{?dist}
Epoch:          1
License:        GPLv2+
URL:            https://opensource.google.com/projects/tesseract
Summary:        Raw OCR Engine
Group:          System Environment/Daemons
Provides:       %{name} = %{epoch}:%{version}-%{release}
Source0:        https://github.com/tesseract-ocr/tesseract/archive/%{version}.tar.gz#/tesseract-%{version}.tar.gz
Source1:        https://github.com/tesseract-ocr/tessdata/raw/%{tessdata_version}/osd.traineddata
Source2:        https://github.com/tesseract-ocr/tessdata/raw/%{tessdata_version}/eng.traineddata
BuildRequires:  automake libtool gcc-c++
BuildRequires:  leptonica-devel >= 1.76.0
BuildRequires:  libicu-devel pango-devel cairo-devel
BuildRequires:  giflib-devel libjpeg-devel openjpeg2-devel libpng-devel libtiff-devel libwebp-devel zlib-devel

# {{{ description
%description
Tesseract OCR engine.
# }}}

# {{{ prep
%prep
%setup -n tesseract-%{version}
# }}}

# {{{ build
%build
autoreconf -ifv

%configure

make %{_smp_mflags}
# }}}

# {{{ install
%install
make install DESTDIR=$RPM_BUILD_ROOT

install -m644 %{SOURCE1} %{buildroot}/%{_datadir}/tessdata
install -m644 %{SOURCE2} %{buildroot}/%{_datadir}/tessdata
# }}}

%ldconfig_scriptlets

# {{{ files
%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_datadir}/*
%exclude %{_datadir}/tessdata/*.traineddata
# }}}

# {{{ package devel
%package devel
Summary:        Tesseract development files
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.la
# }}}

# {{{ package osd
%package osd
Summary:        Tesseract OSD trained data
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description osd

%files osd
%defattr(-,root,root)
%{_datadir}/tessdata/osd.traineddata
# }}}

# {{{ package tesseract-langpack-eng
%package -n tesseract-langpack-eng
Summary:        Tesseract English trained data
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n tesseract-langpack-eng

%files -n tesseract-langpack-eng
%defattr(-,root,root)
%{_datadir}/tessdata/eng.traineddata
# }}}
