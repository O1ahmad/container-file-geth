<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ethereum-icon-purple.svg/1200px-Ethereum-icon-purple.svg.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![0x0I](https://circleci.com/gh/0x0I/container-file-geth.svg?style=svg)](https://circleci.com/gh/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/geth?style=flat)](https://hub.docker.com/repository/docker/0labs/geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

Container file that configures and runs [Geth](https://geth.ethereum.org): a command-line interface and API server for operating an Ethereum node.

## Overview
  - [Configuration](#configuration)
    - [command-line flags](#command-line-flags)
    - [config.toml](#config.toml)
  - [Operations](#operations)
    - [Check account balances](#check-account-balances)
    - [View client sync progress](#view-client-sync-progress)
    - [Backup and encrypt keystore](#backup-keystore)
    - [Import keystore backup](#import-backup)
  - [Examples](#examples)

### Configuration

`geth` can be configured using either runtime command-line flags or a settings file written in [TOML](https://github.com/toml-lang/toml), a minimal configuration language format.

#### command-line flags

See [here](https://geth.ethereum.org/docs/interface/command-line-options) for a list of supported flags.

```bash
# connect to Ethereum mainnet and enable HTTP-RPC service 
docker run 0labs/geth:latest --mainnet --http
```

#### config.toml

_The content of the TOML configuration file can either be pregenerated and mounted into a container instance. e.g:_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

# mount custom config into container
$ docker run --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/config.toml 0labs/geth:latest --config /tmp/config.toml
```

_...created from a set of environment variables, prefixed with `CONFIG`:_

```bash
$ cat custom-config.env
CONFIG_Eth_SyncMode="fast"
CONFIG_Node_DataDir="/mnt/data/geth"

# mount custom config into container
$ docker run -it --env-file custom-config.env 0labs/geth:latest
```

_...or developed from both (with config environment variables taking precedence and overriding mounted config settings):_

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

    A list of configurable settings can be found [here](https://gist.github.com/0x0I/5887dae3cdf4620ca670e3b194d82cba).

    **Note:** `<section-keyword>` should be written with the word 'dot' replacing '.' characters in config section settings (**e.g.** *Node.P2P* should be written as *NodedotP2P*).

### Operations

...

#### Check account balances

Display account balances of all accounts currently managed by a designated `geth` client.

`$GETH_CONFIG_DIR=</path/to/configuration/dir>` (**default**: `/root/.ethereum/geth`)
- container path where the `geth` TOML configuration should be maintained

```bash
GETH_CONFIG_DIR=/mnt/etc/geth
```

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
