#!/bin/bash

exec /opt/geth/geth $EXTRA_ARGS --config "${GETH_CONFIG_DIR:-/etc/geth}/geth.toml"
