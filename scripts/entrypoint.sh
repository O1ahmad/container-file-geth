#!/bin/bash
set -euo pipefail

# Print all commands executed if DEBUG mode enabled
[ -n "${DEBUG:-""}" ] && set -x

DIR=/docker-entrypoint.d

if [[ -d "$DIR" ]] ; then
  /bin/run-parts --exit-on-error "$DIR"
fi

if [[ -n "${GETH_CONFIG_DIR:-""}" ]]; then
  run_args="--config=${GETH_CONFIG_DIR}/config.toml ${EXTRA_ARGS:-}"
else
  run_args=${EXTRA_ARGS:-""}
fi

if [[ -n "${run_args:-""}" ]]; then
  exec /usr/bin/tini -g -- $@ ${run_args}
else
  exec /usr/bin/tini -g -- "$@"
fi
