#!/bin/bash

set -euo pipefail

# If glob doesn't match anything, return empty string rather literal pattern
shopt -s nullglob

# Print all commands executed if DEBUG mode enabled
[ -n "${DEBUG:-""}" ] && set -x

# Execute or source non-executable additional entrypoint scripts. This provides a way for downstream
# images to execute additional setup logic before switching to the `app` user.
for script in /entrypoint.d/*; do
  if [ -x "$script" ]; then
    "$script" "$@"
  else
    # Sourcing scripts allows them to set environment variables and do other
    # dangerous things, so use them sparingly.
    source "$script"
  fi
done

exec "$@"
