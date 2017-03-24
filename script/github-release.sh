#!/bin/sh

set -xe

ERLANG_VERSION=$(grep "%define \+erlver" $HOME/$CIRCLE_PROJECT_REPONAME/erlang.spec | awk '{print $3}')

need_to_release() {
	http_code=$(curl -sL -w "%{http_code}\\n" https://github.com/${CIRCLE_PROJECT_USERNAME}/${CIRCLE_PROJECT_REPONAME}/releases/tag/${ERLANG_VERSION} -o /dev/null)
	test $http_code = "404"
}

if ! need_to_release; then
	echo "$CIRCLE_PROJECT_REPONAME $ERLANG_VERSION has already released."
	exit 0
fi

go get github.com/aktau/github-release
cp $CIRCLE_ARTIFACTS/*.rpm .

#
# Create a release page
#

github-release release \
  --user $CIRCLE_PROJECT_USERNAME \
  --repo $CIRCLE_PROJECT_REPONAME \
  --tag $ERLANG_VERSION \
  --name "Erlang-${ERLANG_VERSION}" \
  --description "not release"

#
# Upload rpm files and build a release note
#

print_rpm_markdown() {
  RPM_FILE=$1
  cat <<EOS
* $RPM_FILE
    * sha256: $(openssl sha256 $RPM_FILE | awk '{print $2}')
EOS
}

upload_rpm() {
  RPM_FILE=$1
  github-release upload --user $CIRCLE_PROJECT_USERNAME \
    --repo $CIRCLE_PROJECT_REPONAME \
    --tag $ERLANG_VERSION \
    --name "$RPM_FILE" \
    --file $RPM_FILE
}

cat <<EOS > description.md
Use at your own risk!

EOS

for i in *.rpm; do
  print_rpm_markdown $i >> description.md
  upload_rpm $i
done

#
# Make the release note to complete!
#

github-release edit \
  --user $CIRCLE_PROJECT_USERNAME \
  --repo $CIRCLE_PROJECT_REPONAME \
  --tag $ERLANG_VERSION \
  --name "Erlang-${ERLANG_VERSION}" \
  --description "$(cat description.md)"
