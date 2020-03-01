<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://retohercules.com/images/ethereum-png-11.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![Build Status](https://travis-ci.org/0x0I/container-file-geth.svg?branch=master)](https://travis-ci.org/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/0x01.geth?style=flat)](https://hub.docker.com/repository/docker/0labs/0x01.geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

**Table of Contents**
  - [Supported Platforms](#supported-platforms)
  - [Requirements](#requirements)
  - [Environment Variables](#environment-variables)
      - [Install](#install)
      - [Config](#config)
      - [Launch](#launch)
  - [Dependencies](#dependencies)
  - [Example Run](#example-run)
  - [License](#license)
  - [Author Information](#author-information)

Container file that installs, configures and runs [Geth](https://geth.ethereum.org): a command-line interface and API server for operating an Ethereum node.

##### Supported Platforms:
```
* Redhat(CentOS/Fedora)
* Debian
```

Requirements
------------

None

Environment Variables
--------------
Variables are available and organized according to the following software & machine provisioning stages:
* _config_
* _launch_

#### Config

Configuration of the `geth` client can be expressed in a config file written in [TOML](https://github.com/toml-lang/toml), a minimal markup language, used as an alternative to passing command-line flags at runtime. To get an idea how the config should look you can use the `geth dumpconfig` subcommand to export a client's existing configuration.

_The following variables can be customized to manage the location and content of this TOML configuration:_

`$GETH_CONFIG_DIR=</path/to/configuration/dir>` (**default**: `/etc/geth`)
- path on target host where the `geth` TOML configuration should be stored

```bash
GETH_CONFIG_DIR=/mnt/etc/geth
```
 
`CONFIG_<section-keyword>_<section-property> = <property-value (string)> **default**: None`

* Any configuration setting/value key-pair supported by `geth` should be expressible within each `CONFIG_*` environment variable and properly rendered within the associated TOML config. note: <section-keyword> should be written as is and expected to be rendered within the associated `TOML` config (e.g. Node.P2P).

  Furthermore, configuration is not constrained by hardcoded author defined defaults or limited by pre-baked templating. If the config section, setting and value are recognized by the `geth` tool, :thumbsup: to define within `geth_config`.

  A list of configurable settings can be found [here](https://gist.github.com/0x0I/5887dae3cdf4620ca670e3b194d82cba).

  Keys of the `geth_config` hash represent TOML config sections:
  ```yaml
  geth_config:
    # [TOML Section 'Shh']
    Shh: {}
  ```

  Values of `geth_config[<key>]` represent key,value pairs within an embedded hash expressing config settings:
  ```yaml
  geth_config:
    # TOML Section '[Shh]'
    Shh:
      # Section setting MaxMessageSize with value of 1048576
      MaxMessageSize: 1048576
  ```

#### Launch

Running the `geth` client and API server, either in its RPC, IPC or WS-RPC form, is accomplished utilizing the [systemd](https://www.freedesktop.org/wiki/Software/systemd/) or [launchd](https://www.launchd.info/) service management tools, for Linux and MacOS platforms respectively. Launched as background processes or daemons subject to the configuration and execution potential provided by the underlying management frameworks, the `geth` client and API servers can be set to adhere to system administrative policies right for your environment and organization.

_The following variables can be customized to manage Geth's execution profile/policy:_

`extra_run_args: <geth-cli-options>` (**default**: see `defaults/main.yml`)
- list of `geth` commandline arguments to pass to the binary at runtime for customizing launch.

Supporting full expression of `geth`'s cli, this variable enables the role of target hosts to be customized according to the user's specification; whether to activate a particular API protocol listener, connect to a pre-configured Ethereum test or production network or whatever is supported by `geth`.

  A list of available command-line options can be found [here](https://gist.github.com/0x0I/a06e231d4fd0509ddf3a44f8499a2941).

##### Examples

  Connect to either the Ropsten PoW(proof-of-work) or Rinkeby PoA(proof-of-authory) pre-configured test network:
  ```
  extra_run_args:
    - '--testnet' # PoW
  # ...or...
  extra_run_args:
    - '--rinkeby' # PoA
  ```

  Enhance logging and debugging capabilities for troubleshooting issues:
  ```
  extra_run_args:
    - --debug
    - '--verbosity 5'
    - '--trace /tmp/geth.trace'
  ```

  Enable client and server profiling for analytics and testing purposes:
  ```
  extra_run_args:
    - --pprof
    - '--memprofilerate 1048576'
    - '--blockprofilerate 1'
    - '--cpuprofile /tmp/geth-cpu-profile'
  ```

`custom_unit_properties: <hash-of-systemd-service-settings>` (**default**: `[]`)
- hash of settings used to customize the `[Service]` unit configuration and execution environment of the *Geth* **systemd** service.

Dependencies
------------

- 0x0i.systemd

Example Playbook
----------------
Basic setup with defaults:
```
- hosts: all
  roles:
  - role: 0x0I.geth
```

Launch an Ethereum light client and connect it to the Rinkeby PoA (Proof of Authority) test network:
```
- hosts: light-client
  roles:
  - role: 0x0I.geth
    vars:
      geth_config:
        Eth:
          SyncMode: light
      extra_run_args:
        - --rinkeby
```

Run a full Ethereum node using "fast" sync-mode (only process most recent transactions), enabling both the RPC server interface and client miner and overriding the (block) data directory:
```
- hosts: full-node
  roles:
  - role: 0x0I.geth
    vars:
      geth_config:
        Eth:
          SyncMode: fast
        Node:
          DataDir: /mnt/geth
      extra_run_args:
        - --rpc
        - '--rpcaddr="0.0.0.0'
        - '--mine --miner.threads 16'
```

License
-------

MIT

Author Information
------------------

This role was created in 2020 by O1.IO.
