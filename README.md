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
 
`$CONFIG_<section-keyword>_<section-property> = <property-value (string)>` **default**: *None*

* Any configuration setting/value key-pair supported by `geth` should be expressible within each `CONFIG_*` environment variable and properly rendered within the associated TOML config. **Note:** `<section-keyword>` along with the other property specifications should be written as expected to be rendered within the associated `TOML` config (**e.g.** *Node.P2P*).

Furthermore, configuration is not constrained by hardcoded author defined defaults or limited by pre-baked templating. If the config section, setting and value are recognized by the `geth` tool, :thumbsup: to define within an environnment variable according to the following syntax.

  A list of configurable settings can be found [here](https://gist.github.com/0x0I/5887dae3cdf4620ca670e3b194d82cba).

  `<section-keyword>` -- represents TOML config sections:
  ```bash
  # [TOML Section 'Shh']
  CONFIG_Shh_<section-property>=<property-value>
  ```
  
  `<section-property>` -- represents a specific TOML config section property to configure:
  
  ```bash
  # [TOML Section 'Shh']
  # Property: MaxMessageSize
  CONFIG_Shh_MaxMessageSize=<property-value>
  ```

  `<property-value>` -- represents property value to configure:
  ```bash
  # [TOML Section 'Shh']
  # Property: MaxMessageSize
  # Value: 2097152
  CONFIG_Shh_MaxMessageSize=2097152
  ```

#### Launch

Running the `geth` client and API server, either in its RPC, IPC or WS-RPC form, is accomplished utilizing official **Geth** binaries published and available [here](https://github.com/ethereum/go-ethereum/releases). Launched subject to the configuration and execution potential provided by the underlying application, the `geth` client and API servers can be set to adhere to system administrative policies right for your environment and organization.

_The following variables can be customized to manage Geth's execution profile/policy:_

`$EXTRA_ARGS: <geth-cli-options>` (**default**: *NONE*)
- list of `geth` commandline arguments to pass to the binary at runtime for customizing launch.

Supporting full expression of `geth`'s cli, this variable enables the role of target hosts to be customized according to the user's specification; whether to activate a particular API protocol listener, connect to a pre-configured Ethereum test or production network or whatever is supported by `geth`.

  A list of available command-line options can be found [here](https://gist.github.com/0x0I/a06e231d4fd0509ddf3a44f8499a2941).

##### Examples

  Connect to either the Ropsten PoW(proof-of-work) or Rinkeby PoA(proof-of-authory) pre-configured test network:
  ```bash
  EXTRA_ARGS=--testnet # POW
  # ...or...
  EXTRA_ARGS=--rinkeby # POA
  ```

  Enhance logging and debugging capabilities for troubleshooting issues:
  ```bash
  EXTRA_ARGS=--debug --verbosity 5 --trace /tmp/geth.trace
  ```

  Enable client and server profiling for analytics and testing purposes:
  ```
  EXTRA_ARGS=--pprof --memprofilerate 1048576 --blockprofilerate 1 --cpuprofile /tmp/geth-cpu-profile
  ```

Dependencies
------------

None

Example Run
----------------
Basic setup with defaults:
```
podman run 0labs/0x01.geth:centos-7
```

Launch an Ethereum light client and connect it to the Rinkeby PoA (Proof of Authority) test network:
```
podman run --env CONFIG_Eth_SyncMode='"light"' --env EXTRA_ARGS=--rinkeby 0labs/0x01.geth:centos-7
```

Run a full Ethereum node using "fast" sync-mode (only process most recent transactions), enabling both the RPC server interface and overriding the (block) data directory:
```
podman run --env CONFIG_Eth_SyncMode='"fast"' \
           --env CONFIG_Node_DataDir='"/mnt/geth/data"' \
           --env EXTRA_ARGS="--rpc" \
           --volume geth_data:/mnt/geth/data
           0labs/0x01.geth:centos-7
```

License
-------

MIT

Author Information
------------------

This Container file was created in 2020 by O1.IO.
