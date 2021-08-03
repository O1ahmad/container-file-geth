<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ethereum-icon-purple.svg/1200px-Ethereum-icon-purple.svg.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![0x0I](https://circleci.com/gh/0x0I/container-file-geth.svg?style=svg)](https://circleci.com/gh/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/geth?style=flat)](https://hub.docker.com/repository/docker/0labs/geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

Container file that configures and runs [Geth](https://geth.ethereum.org): a command-line interface and API server for operating an Ethereum node.

**Overview**
  - [Requirements](#requirements)
  - [Environment Variables](#environment-variables)
      - [Config](#config)
      - [Operations](#operations)
        - [check account balances](#check-account-balances)
        - [view client sync progress](#view-client-sync-progress)
        - [backup and encrypt keystore](#backup-and-encrypt-keystore)
        - [import backup](#import-backup)
  - [Examples](#examples)
  - [License](#license)
  - [Author Information](#author-information)

Requirements
------------

None

Environment Variables
--------------

Variables are available and organized according to the following software & machine provisioning stages:
* _config_
* _operations_

### :page_with_curl: Config

Configuration of the `geth` client can be expressed in a config file written in [TOML](https://github.com/toml-lang/toml), a minimal markup format, used as an alternative to passing command-line flags at runtime. To get an idea how the config should look you can use the `geth dumpconfig` subcommand to export a client's existing configuration.

_The following variables can be customized to manage the location and content of this TOML configuration:_

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

_Additionally, the content of the TOML configuration file can either be pregenerated and mounted into a container instance:_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

# mount custom config into container
$ docker run --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/config.toml 0labs/geth:latest --config /tmp/config.toml
```

_...or developed from both a mounted config and injected environment variables (with envvars taking precedence and overriding mounted config settings):_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

# mount custom config into container
$ docker run -it --env GETH_CONFIG_DIR=/tmp/geth --env CONFIG_Eth_SyncMode=full \
  --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/geth/config.toml \
  0labs/geth:latest --config /tmp/geth/config.toml
```

_Moreover, see [here](https://geth.ethereum.org/docs/interface/command-line-options) for a list of supported flags to set as runtime command-line flags._

```bash
# connect to Ethereum mainnet and enable HTTP-RPC service 
docker run 0labs/geth:latest --mainnet --http
```

### :flashlight: Operations

To assist with managing a `geth` client and interfacing with the *Ethereum* network, the following utility functions have been included within the image.

#### Check account balances

Display account balances of all accounts currently managed by a designated `geth` RPC server.

```
$ geth-helper status check-balances --help
Usage: geth-helper status check-balances [OPTIONS]

  Check all client managed account balances

Options:
  --rpc-addr TEXT  server address to query for RPC calls  [default:
                   (http://localhost:8545)]
  --help           Show this message and exit.
```

`$RPC_ADDRESS=<web-address>` (**default**: `localhost:8545`)
- `geth` RPC server address for querying network state

##### example

```bash
docker exec --env RPC_ADDRESS=geth-rpc.live.01labs.net 0labs/geth:latest geth-helper status check-balances
```

#### View client sync progress

View current progress of an RPC server's sync with the network if not already caughtup.

```
$ geth-helper status sync-progress --help
Usage: geth-helper status sync-progress [OPTIONS]

  Check client blockchain sync status and process

Options:
  --rpc-addr TEXT  server address to query for RPC calls  [default:
                   (http://localhost:8545)]
  --help           Show this message and exit
```

`$RPC_ADDRESS=<web-address>` (**default**: `localhost:8545`)
- `geth` RPC server address for querying network state

The progress output consists of a JSON block with the following properties:
  * __progress__ - percent (%) of total blocks processed and synced by the server
  * __blocksToGo__ - number of blocks left to process/sync
  * __bps__: rate of blocks processed/synced per second
  * __percentageIncrease__ - progress percentage increase since last view
  * __etaHours__ - estimated time (hours) to complete sync

##### example

```bash
$ docker exec --env RPC_ADDRESS=geth-rpc.live.01labs.net 0labs/geth:latest geth-helper status sync-progress [--rpc-address geth-rpc.live.01labs.net]

  {
   "progress":66.8226399830796,
   "blocksToGo":4298054,
   "bps":5.943412173361741,
   "percentageIncrease":0.0018371597201962686,
   "etaHours":200.87852803477827
  }
```

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
