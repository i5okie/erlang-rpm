%undefine _missing_build_ids_terminate_build
%define erlver  19.3

Name:           erlang
Summary:        Erlang OTP package
Version:        %{erlver}
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://www.erlang.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ncurses glibc openssl zlib
BuildRequires:  ncurses-devel glibc-devel gcc openssl-devel make zlib-devel chrpath
Source0:        http://erlang.org/download/otp_src_%{erlver}.tar.gz
Group:          Development/Languages
Packager:       <ryohei-sonoda@outlook.com>
Obsoletes:      esl-erlang
Obsoletes:      esl-erlang-compat
Obsoletes:      erlang
Obsoletes:      erlang-appmon
Obsoletes:      erlang-asn1
Obsoletes:      erlang-common_test
Obsoletes:      erlang-compiler
Obsoletes:      erlang-cosEvent
Obsoletes:      erlang-cosEventDomain
Obsoletes:      erlang-cosFileTransfer
Obsoletes:      erlang-cosNotification
Obsoletes:      erlang-cosProperty
Obsoletes:      erlang-cosTime
Obsoletes:      erlang-cosTransactions
Obsoletes:      erlang-crypto
Obsoletes:      erlang-debugger
Obsoletes:      erlang-dialyzer
Obsoletes:      erlang-diameter
Obsoletes:      erlang-docbuilder
Obsoletes:      erlang-edoc
Obsoletes:      erlang-erl_docgen
Obsoletes:      erlang-erl_interface
Obsoletes:      erlang-erts
Obsoletes:      erlang-et
Obsoletes:      erlang-eunit
Obsoletes:      erlang-examples
Obsoletes:      erlang-gs
Obsoletes:      erlang-hipe
Obsoletes:      erlang-ic
Obsoletes:      erlang-inets
Obsoletes:      erlang-inviso
Obsoletes:      erlang-jinterface
Obsoletes:      erlang-kernel
Obsoletes:      erlang-megaco
Obsoletes:      erlang-mnesia
Obsoletes:      erlang-observer
Obsoletes:      erlang-odbc
Obsoletes:      erlang-orber
Obsoletes:      erlang-os_mon
Obsoletes:      erlang-otp_mibs
Obsoletes:      erlang-parsetools
Obsoletes:      erlang-percept
Obsoletes:      erlang-pman
Obsoletes:      erlang-public_key
Obsoletes:      erlang-reltool
Obsoletes:      erlang-runtime_tools
Obsoletes:      erlang-sasl
Obsoletes:      erlang-snmp
Obsoletes:      erlang-ssh
Obsoletes:      erlang-ssl
Obsoletes:      erlang-stdlib
Obsoletes:      erlang-syntax_tools
Obsoletes:      erlang-test_server
Obsoletes:      erlang-toolbar
Obsoletes:      erlang-tools
Obsoletes:      erlang-tv
Obsoletes:      erlang-typer
Obsoletes:      erlang-webtool
Obsoletes:      erlang-wx
Obsoletes:      erlang-xmerl

%description
Erlang is a programming language used to build massively scalable soft real-time systems with requirements on high availability.
Some of its uses are in telecoms, banking, e-commerce, computer telephony and instant messaging.
Erlang's runtime system has built-in support for concurrency, distribution and fault tolerance.

%prep
%setup -q -n otp_src_%{erlver}

%build
%global conf_flags --enable-shared-zlib --without-javac --without-odbc --enable-dirty-schedulers
./otp_build autoconf
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %configure %{conf_flags}
make clean
touch lib/cosEvent/SKIP
touch lib/cosEventDomain/SKIP
touch lib/cosFileTransfer/SKIP
touch lib/cosNotification/SKIP
touch lib/cosProperty/SKIP
touch lib/cosTime/SKIP
touch lib/cosTransactions/SKIP
touch lib/jinterface/SKIP
touch lib/megaco/SKIP
touch lib/odbc/SKIP
touch lib/orber/SKIP
touch lib/test_server/SKIP
make -j4

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir}/erlang -type f -name info -delete
rm -rf %{buildroot}%{_libdir}/erlang/erts-*/man
rm -rf %{buildroot}%{_libdir}/erlang/Install

for exe in %{buildroot}%{_libdir}/erlang/erts-*/bin/*
do
    base="$(basename "$exe")"
    next="%{buildroot}%{_libdir}/erlang/bin/${base}"
    rel="$(echo "$exe" | sed "s,^%{buildroot}%{_libdir}/erlang/,../,")"
    if cmp "$exe" "$next"; then
        ln -sf "$rel" "$next"
        fi
done
for exe in %{buildroot}%{_libdir}/erlang/bin/*
do
    base="$(basename "$exe")"
    next="%{buildroot}%{_bindir}/${base}"
    rel="$(echo "$exe" | sed "s,^%{buildroot},,")"
    if cmp "$exe" "$next"; then
        ln -sf "$rel" "$next"
        fi
done

chrpath -d %{buildroot}%{_libdir}/erlang/lib/crypto-*/priv/lib/crypto.so

%post
echo "Erlang OTP %{erlver} installed"

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_bindir}/*

%clean
rm -rf %{buildroot}{_libdir}/*
