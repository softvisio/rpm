%define version %(git ls-remote --tags git://github.com/antirez/redis.git | perl -lne 'm[refs/tags/([\\d.]+)$]sm ? print $1 : next' | sort -V | tail -n 1)

# allow to download sources
%undefine _disable_source_fetch

# disable debug package build
%define debug_package %{nil}
%define debug_packages %{nil}

Name:          redis
Version:       %{version}
Release:       4%{?dist}
Epoch:         1
License:       GPLv2+
URL:           https://redis.io/
Summary:       A persistent key-value database
Group:         System Environment/Daemons
Provides:      %{name} = %{epoch}:%{version}-%{release}
Source0:       https://github.com/antirez/redis/archive/%{version}.tar.gz

# "tcl" is required for redis server tests
# "which" is required by redis run-test script
BuildRequires: which tcl

# {{{ description
%description
Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.
# }}}

# {{{ prep
%prep

%setup
# }}}

# {{{ build
%build

# disable Redis protected mode [1] as it is unnecessary in context of Docker
# (ports are not automatically exposed when running inside Docker, but rather explicitly by specifying -p / -P)
# [1]: https://github.com/antirez/redis/commit/edd4d555df57dc84265fdfb4ef59a4678832f6da

# grep -q '\''^#define CONFIG_DEFAULT_PROTECTED_MODE 1$'\'' /usr/src/redis-stable/src/server.h
# sed -ri '\''s!^(#define CONFIG_DEFAULT_PROTECTED_MODE) 1$!\1 0!'\'' /usr/src/redis-stable/src/server.h
# grep -q '\''^#define CONFIG_DEFAULT_PROTECTED_MODE 0$'\'' /usr/src/redis-stable/src/server.h

# for future reference, we modify this directly in the source instead of just supplying a default configuration flag because apparently "if you specify any argument to redis-server, [it assumes] you are going to specify everything"
# see also https://github.com/docker-library/redis/issues/4#issuecomment-50780840
# (more exactly, this makes sure the default behavior of "save on SIGTERM" stays functional by default)

make %{_smp_mflags}
# }}}

# {{{ install
%install

make install INSTALL="install -p" PREFIX=$RPM_BUILD_ROOT%{_prefix}
# }}}

# {{{ files
%files

%defattr(-,root,root,-)
%{_bindir}/*
# }}}
