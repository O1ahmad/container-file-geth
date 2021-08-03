<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ethereum-icon-purple.svg/1200px-Ethereum-icon-purple.svg.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![0x0I](https://circleci.com/gh/0x0I/container-file-geth.svg?style=svg)](https://circleci.com/gh/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/geth?style=flat)](https://hub.docker.com/repository/docker/0labs/geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

Container file that configures and runs [Geth](https://geth.ethereum.org): a command-line interface and API server for operating an Ethereum node.

## Table of Contents
  - [Config](#config)
  - [Operations](#operations)
  - [Example Run](#example-run)

### Config

Configuration of the `geth` client can be expressed in a config file written in [TOML](https://github.com/toml-lang/toml), a minimal markup language, used as an alternative to passing command-line flags at runtime. To get an idea how the config should look you can use the `geth dumpconfig` subcommand to export a client's existing configuration.

_The content of this TOML configuration file can either be pregenerated and mounted into a container instance:_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

[Node.P2P]
BootstrapNodes = ["enode://a979fb575495b8d6db44f750317d0f4622bf4c2aa3365d6af7c284339968eef29b69ad0dce72a4d8db5ebb4968de0e3bec910127f134779fbcb0cb6d3331163c@52.16.188.185:30303"]

# mount custom config into container
$ docker run -it --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/config.toml \
  0labs/geth:latest --config /tmp/config.toml
```

_generated from a set of environment variables, prefixed with `CONFIG`:_

```bash
$ cat custom-config.env
CONFIG_Eth_SyncMode="fast"
CONFIG_Node_DataDir="/mnt/data/geth"
CONFIG_NodedotP2P_BootstrapNodes=["enode://a979fb575495b8d6db44f750317d0f4622bf4c2aa3365d6af7c284339968eef29b69ad0dce72a4d8db5ebb4968de0e3bec910127f134779fbcb0cb6d3331163c@52.16.188.185:30303"]

# mount custom config into container
$ docker run -it --env-file custom-config.env 0labs/geth:latest
```

_or created from both (with config environment variables taking precedence) and overriding mounted config settings:_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

$ cat custom-config.env
GETH_CONFIG_DIR=/tmp/geth
CONFIG_Eth_SyncMode="full"

# mount custom config into container
$ docker run -it --env-file custom-config.env \
  --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/geth/config.toml \
  0labs/geth:latest --config /tmp/geth/config.toml
```

`$GETH_CONFIG_DIR=</path/to/configuration/dir>` (**default**: `/root/.ethereum/geth`)
- container path where the `geth` TOML configuration should be maintained

```bash
GETH_CONFIG_DIR=/mnt/etc/geth
```

`$CONFIG_<section-keyword>_<section-property> = <property-value (string)>` **default**: *None*

- Any configuration setting/value key-pair supported by `geth` should be expressible and properly rendered within the associated TOML config.

**Note:** `<section-keyword>` should be written with the word 'dot' replacing '.' characters in config section settings (**e.g.** *Node.P2P* should be written as *NodedotP2P*).

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

### Operations

Included within the image is a helper tool, `geth-helper`, which provides advanced capabilities for operating
a geth client. The supported operations are as follows.

- [Check account balances](#check-account-balances)
- [Check client sync progress](#check-client-sync-progress)
- [Backup and encrypt keystore](#backup-keystore)
- [Import backup](#import-backup)

#### Check account balances

...

#### Check client sync progress

...

#### Backup and encrypt keystore

...

#### Import backup

...

Example Run
----------------

Create account:
```
docker run -it 0labs/geth:latest
```

Launch an Ethereum light client and connect it to the Rinkeby PoA (Proof of Authority) test network:
```
docker run --env CONFIG_Eth_SyncMode=light 0labs/geth:latest --rinkeby
```

Run a full Ethereum node using "fast" sync-mode (only process most recent transactions), enabling both the RPC server interface and overriding the (block) data directory:
```
docker run --env CONFIG_Eth_SyncMode=fast \
           --env CONFIG_Node_DataDir="/mnt/geth/data" \
           --volume geth_data:/root/.ethereum
           0labs/geth:latest --rpc
```

License
-------

MIT

Author Information
------------------

This Containerfile was created in 2021 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

**Eth:** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c
