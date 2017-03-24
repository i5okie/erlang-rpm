#!/bin/sh
set -xe
OS_VERSION=$1
DOCKER_IMAGE=${OS_VERSION}/erlang-rpm
docker run -u builder -v $CIRCLE_ARTIFACTS:/shared:rw $DOCKER_IMAGE ./build-erlang.sh
