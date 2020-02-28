#!/bin/bash

set -euo pipefail

# Print all commands executed if DEBUG mode enabled
[ -n "${DEBUG:-""}" ] && set -x

# [Test-Setup]
cat <<OS | xargs -I % docker build --file Containerfile --build-arg OS_VERSION=% --build-arg ARCHIVE_URL --tag geth-testing-% .
centos:7
centos:8
fedora:29
fedora:30
fedora:31
OS

# [Test-Run+Validate]
export GOSS_FILES_PATH=test
cat <<OS | xargs -I % dgoss run --env-file test/config-test.env geth-testing-%
centos:7
centos:8
fedora:29
fedora:30
fedora:31
OS
unset GOSS_FILES_PATH
