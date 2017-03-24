#!/bin/sh

set -xe

OS_VERSION=$1

DOCKER_ARCHIVE_PATH=$HOME/cache/${OS_VERSION}-erlang-rpm.tar.gz
DOCKER_IMAGE=${OS_VERSION}/erlang-rpm
DOCKER_FILE=Dockerfile-${OS_VERSION}

MD5_DIGEST_SOURCE=md5_digest.source-${OS_VERSION}
MD5_DIGEST_PATH=$HOME/cache/dockerfile${OS_VERSION}.digest

can_use_cache() {
  test -e $DOCKER_ARCHIVE_PATH &&
    md5sum --status --quiet --check $MD5_DIGEST_PATH > /dev/null 2>&1
}

md5_digest_source() {
  # Consider Dockerfile and the related files
  cat $DOCKER_FILE $(grep '^ADD ' $DOCKER_FILE | awk '{$1=""; $NF=""; print $0}')
}

if [ ! -f "$DOCKER_FILE" ]; then
  echo "$DOCKER_FILE is not exist." >&2
  exit 1
fi

cd $HOME/$CIRCLE_PROJECT_REPONAME

md5_digest_source > $MD5_DIGEST_SOURCE

if can_use_cache; then
  docker load < $DOCKER_ARCHIVE_PATH
else
  mkdir -p $HOME/cache
  md5sum $MD5_DIGEST_SOURCE > $MD5_DIGEST_PATH
  docker build -t $DOCKER_IMAGE -f $DOCKER_FILE .
  docker save $DOCKER_IMAGE | gzip -c > $DOCKER_ARCHIVE_PATH
fi

docker info
