%define version %(git ls-remote --tags git://github.com/alibaba/tengine.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          tengine
Version:       %{version}
Release:       1%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://github.com/alibaba/tengine/
Summary:       A high performance web server and reverse proxy server
Group:         System Environment/Daemons
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://tengine.taobao.org/download/tengine-%{version}.tar.gz
BuildRequires: pcre-devel zlib-devel openssl-devel libmaxminddb-devel

# {{{ description
%description
Tengine is a web server and a reverse proxy server for HTTP, SMTP, POP3 and IMAP protocols, with a strong focus on high concurrency, performance and low memory usage.
# }}}

# {{{ prep
%prep

%setup -n tengine-%{version}

# git clone https://github.com/softvisio/ngx_http_geoip2
# git clone https://github.com/softvisio/ngx_dynamic_upstream

# }}}

# {{{ build
%build

    # --user=%{nginx_user} \
    # --group=%{nginx_user} \

    # --with-http_xslt_module=dynamic \
    # --with-http_image_filter_module=dynamic \
    # --with-http_perl_module=dynamic \
    # --with-mail=dynamic \
    # --with-mail_ssl_module \
    # --with-http_dav_module \


./configure \
    --sbin-path=%{_prefix}/local/sbin/nginx \
    --with-threads \
    --with-file-aio \
    --with-pcre \
    --with-pcre-jit \
    --with-stream \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --with-ld-opt="$RPM_LD_FLAGS -Wl,-E" `# so the perl module finds its symbols` \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_degradation_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-stream_ssl_module \
    --add-dynamic-module=ngx_http_geoip2 \
    --add-module=ngx_dynamic_upstream

make %{_smp_mflags}
# }}}

# {{{ install
%install

make install DESTDIR=$RPM_BUILD_ROOT
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_prefix}/local/sbin/nginx
%{_prefix}/local/nginx/*
# }}}
