#!/bin/sh -xe
ERLANG_VERSION=$(grep "%define \+erlver" erlang.spec | awk '{print $3}')
SOURCE_PATH=$HOME/cache/
if test -e $SOURCE_PATH/otp_src_${ERLANG_VERSION}.tar.gz; then
  echo 'Use local source cache.'
else
  mkdir -p $HOME/cache
  curl -L http://erlang.org/download/otp_src_$ERLANG_VERSION.tar.gz > $SOURCE_PATH/otp_src_$ERLANG_VERSION.tar.gz
fi
