%define erlver  19.3

Name:           erlang
Version:        %{erlver}
Release:        1%{?dist}
License:        Apache Software License 2.0
Url:            https://www.erlang.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ncurses glibc openssl zlib
BuildRequires:  ncurses-devel glibc-devel gcc openssl-devel make zlib-devel
Source0:        http://erlang.org/download/otp_src_%{erlver}.tar.gz
Summary:        Erlang is a programming language used to build massively scalable soft real-time systems with requirements on high availability.
Group:          Development/Languages
Obsoletes:      erlang

%description
Erlang is a programming language used to build massively scalable soft real-time systems with requirements on high availability.
Some of its uses are in telecoms, banking, e-commerce, computer telephony and instant messaging.
Erlang's runtime system has built-in support for concurrency, distribution and fault tolerance.

%prep
%setup -n otp_src_%{erlver}

%build
%configure \
  --without-javac \
  --includedir=%{_includedir}/erlang \
  --libdir=%{_libdir}

make %{?_smp_mflags}

%install
# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

#we don't want to keep the src directory
rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*
