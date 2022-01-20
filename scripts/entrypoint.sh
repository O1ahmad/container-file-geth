#!/bin/bash
set -euo pipefail

# Print all commands executed if DEBUG mode enabled
[ -n "${DEBUG:-""}" ] && set -x

DIR=/docker-entrypoint.d

if [[ -d "$DIR" ]] ; then
  /bin/run-parts --exit-on-error "$DIR"
fi

if [[ -n "${EXTRA_ARGS:-""}" ]]; then
  exec /usr/bin/tini -g -- $@ ${EXTRA_ARGS}
else
  exec /usr/bin/tini -g -- "$@"
fi
