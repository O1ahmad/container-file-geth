#!/bin/bash

exec /opt/geth/geth --nousb --config "${GETH_CONFIG_DIR:-/etc/geth}/geth.toml"
