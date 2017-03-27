#!/bin/sh

set -xe

ERLANG_VERSION=$(grep "%define \+erlver" $HOME/rpmbuild/SPECS/erlang.spec | awk '{print $3}')

cd $HOME/rpmbuild/SOURCES
if ! test -e otp_src_$ERLANG_VERSION.tar.gz; then
  echo 'Missing sources!'
  exit 1
fi

rpmbuild -ba $HOME/rpmbuild/SPECS/erlang.spec

cp $HOME/rpmbuild/RPMS/x86_64/* /shared
cp $HOME/rpmbuild/SRPMS/* /shared
