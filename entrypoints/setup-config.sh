#!/bin/bash

# Print all commands executed if DEBUG mode enabled
[ -n "${DEBUG:-""}" ] && set -x

config_dir="${GETH_CONFIG_DIR:-/etc/geth}"
config_path="${config_dir}/geth.toml"

mkdir -p $config_dir

# Add provisioning header
echo "# Managed by 0xO1.IO" >> $config_path

if env | grep -i CONFIG_; then
  for VAR in `env | sort -h`
  do
    if [[ "$VAR" =~ ^CONFIG_ ]]; then
      property_section=`echo "$VAR" | sed -r "s/CONFIG_(.*)_.*=.*/\1/g" | tr _ .`
      if !(grep "\[${property_section}\]" $config_path); then
        echo >> $config_path
        echo "[${property_section}]" >> $config_path
      fi
      property_key=`echo "$VAR" | sed -r "s/CONFIG_.*_(.*)=.*/\1/g" | tr _ .`
      property_value=`echo "CONFIG_${property_section}_${property_key}"`
      echo "$property_key = ${!property_value}" >> $config_path
    fi
  done
fi
