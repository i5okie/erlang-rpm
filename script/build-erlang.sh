#!/bin/sh

set -xe

ERLANG_X_Y_VERSION=$(grep "%define \+erlver" $HOME/rpmbuild/SPECS/erlang.spec | awk '{print $3}')

cd $HOME/rpmbuild/SOURCES
curl -LO http://erlang.org/download/otp_src_$ERLANG_X_Y_VERSION.tar.gz

rpmbuild -ba $HOME/rpmbuild/SPECS/erlang.spec

cp $HOME/rpmbuild/RPMS/x86_64/* /shared
cp $HOME/rpmbuild/SRPMS/* /shared
