#!/bin/sh
set -xe
OS_VERSION=$1
DOCKER_IMAGE=${OS_VERSION}/erlang-rpm
ERLANG_VERSION=$(grep "%define \+erlver" erlang.spec | awk '{print $3}')
docker run -u builder \
  -v $HOME/cache/otp_src_$ERLANG_VERSION.tar.gz:/home/builder/rpmbuild/SOURCES/otp_src_$ERLANG_VERSION.tar.gz:ro \
  -v $CIRCLE_ARTIFACTS:/shared:rw \
  $DOCKER_IMAGE ./build-erlang.sh
