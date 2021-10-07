<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ethereum-icon-purple.svg/1200px-Ethereum-icon-purple.svg.png" alt="ethereum logo" title="ethereum" align="right" height="100" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![0x0I](https://circleci.com/gh/0x0I/container-file-geth.svg?style=svg)](https://circleci.com/gh/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/geth?style=flat)](https://hub.docker.com/repository/docker/0labs/geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

Configure and operate Geth (Go-Ethereum): an Ethereum blockchain client written in Go.


**Overview**
  - [Setup](#setup)
    - [Build](#build)
    - [Config](#config)
  - [Operations](#operations)
  - [Examples](#examples)
  - [License](#license)
  - [Author Information](#author-information)

### Setup
--------------
Guidelines on running `0labs/geth` containers are available and organized according to the following software & machine provisioning stages:
* _build_
* _config_
* _operations_

#### Build

##### targets

| Name  | description |
| ------------- | ------------- |
| `builder` | image state following build of geth binary/artifacts |
| `test` | image containing test tools, functional test cases for validation and `release` target contents |
| `release` | minimal resultant image containing service binaries, entrypoints and helper scripts |
| `tool` | setup consisting of all geth utilities, helper tooling and `release` target contents |

```bash
docker build --target <target> -t <tag> .
```

#### Config

:page_with_curl: Configuration of the `geth` client can be expressed in a config file written in [TOML](https://github.com/toml-lang/toml), a minimal markup format, used as an alternative to passing command-line flags at runtime. To get an idea how the config should look you can use the `geth dumpconfig` subcommand to export a client's existing configuration. Also, a list of configurable settings can be found [here](https://gist.github.com/0x0I/5887dae3cdf4620ca670e3b194d82cba).

_The following variables can be customized to manage the location and content of this TOML configuration:_

`$GETH_CONFIG_DIR=</path/to/configuration/dir>` (**default**: `/root/.ethereum/geth`)
- container path where the `geth` TOML configuration should be maintained

  ```bash
  GETH_CONFIG_DIR=/mnt/etc/geth
  ```

`$CONFIG-<section-keyword>-<section-property> = <property-value (string)>` **default**: *None*

- Any configuration setting/value key-pair supported by `geth` should be expressible and properly rendered within the associated TOML config.

    `<section-keyword>` -- represents TOML config sections:
    ```bash
    # [TOML Section 'Shh']
    CONFIG-Shh-<section-property>=<property-value>
    ```

    `<section-property>` -- represents a specific TOML config section property to configure:

    ```bash
    # [TOML Section 'Shh']
    # Property: MaxMessageSize
    CONFIG-Shh-MaxMessageSize=<property-value>
    ```

    `<property-value>` -- represents property value to configure:
    ```bash
    # [TOML Section 'Shh']
    # Property: MaxMessageSize
    # Value: 2097152
    CONFIG-Shh-MaxMessageSize=2097152
    ```
    
_Additionally, the content of the TOML configuration file can either be pregenerated and mounted into a container instance:_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

# mount custom config into container
$ docker run --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/config.toml 0labs/geth:latest geth --config /tmp/config.toml
```

_...or developed from both a mounted config and injected environment variables (with envvars taking precedence and overriding mounted config settings):_

```bash
$ cat custom-config.toml
[Eth]
SyncMode = "fast"

[Node]
DataDir = "/mnt/data/geth"

# mount custom config into container
$ docker run -it --env GETH_CONFIG_DIR=/tmp/geth --env CONFIG-Eth-SyncMode=full \
  --mount type=bind,source="$(pwd)"/custom-config.toml,target=/tmp/geth/config.toml \
  0labs/geth:latest geth --config /tmp/geth/config.toml
```

_Moreover, see [here](https://geth.ethereum.org/docs/interface/command-line-options) for a list of supported flags to set as runtime command-line flags._

```bash
# connect to Ethereum mainnet and enable HTTP-RPC service 
docker run 0labs/geth:latest geth --mainnet --http
```

_...and reference below for network/chain identification and communication configs:_ 

###### port mappings

| Port  | mapping description | type | config setting | command-line flag |
| :-------------: | :-------------: | :-------------: | :-------------: | :-------------: |
| `3085`    | RPC server | *TCP*  | `Node : HTTPPort` | `--http.port` |
| `3086`    | Websocket RPC server | *TCP*  | `Node : WSPort` | `--ws.port` |
| `30303`    | protocol peer gossip and discovery | *TCP/UDP*  | `Node.P2P : ListenAddr` | `--port` |
| `6060`    | metrics collections | *TCP*  | `Metrics : Port` | `--metrics.port` |

###### chain id mappings

| name | config setting (Eth : NetworkId) | command-line flag |
| :---: | :---: | :---: |
| Mainnet | 1 | `--mainnet` |
| Goerli | 5 | `--goerli` |
| Kovan | 42 | `n/a` |
| Rinkeby | 4 | `--rinkeby` |
| Ropsten | 3 | `--ropsten` |

see [chainlist.org](https://chainlist.org/) for a complete list

#### Operations

:flashlight: To assist with managing a `geth` client and interfacing with the *Ethereum* network, the following utility functions have been included within the image. *Note:* all tool command-line flags can alternatively be expressed as container runtime environment variables, as described below.

##### Check account balances

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

The balances output consists of a JSON list of entries with the following properties:
  * __account__ - account owner's address
  * __balance__ - total balance of account in decimal

###### example

```bash
docker exec --env RPC_ADDRESS=geth-rpc.live.01labs.net 0labs/geth:latest geth-helper status check-balances

[
  {
   "account": 0x652eD9d222eeA1Ad843efab01E60C29bF2CF6E4c,
   "balance": 1000000
  },
  {
   "account": 0x256eDb444eeA1Ad876efaa160E60C29bF8CH3D9a,
   "balance": 2000000
  }
]
```

##### View client sync progress

View current progress of an RPC server's sync with the network if not already caughtup.

```
$ geth-helper status sync-progress --help
Usage: geth-helper status sync-progress [OPTIONS]

  Check client blockchain sync status and process

Options:
  --rpc-addr TEXT  server address to query for RPC calls  [default:
                   (http://localhost:8545)]
  --help           Show this message and exit.
```

`$RPC_ADDRESS=<web-address>` (**default**: `localhost:8545`)
- `geth` RPC server address for querying network state

The progress output consists of a JSON block with the following properties:
  * __progress__ - percent (%) of total blocks processed and synced by the server
  * __blocksToGo__ - number of blocks left to process/sync
  * __bps__: rate of blocks processed/synced per second
  * __percentageIncrease__ - progress percentage increase since last view
  * __etaHours__ - estimated time (hours) to complete sync

###### example

```bash
$ docker exec 0labs/geth:latest geth-helper status sync-progress

  {
   "progress":66.8226399830796,
   "blocksToGo":4298054,
   "bps":5.943412173361741,
   "percentageIncrease":0.0018371597201962686,
   "etaHours":200.87852803477827
  }
```

##### Backup and encrypt keystore

Encrypt and backup client keystore to designated container/host location.

```
$ geth-helper account backup-keystore --help
Usage: geth-helper account backup-keystore [OPTIONS] PASSWORD

  Encrypt and backup wallet keystores.

  PASSWORD password used to encrypt and secure keystore backups

Options:
  --keystore-dir TEXT  path to import a backed-up geth wallet key store
                       [default: (/root/.ethereum/keystore)]
  --backup-path TEXT   path containing backup of a geth wallet key store
                       [default: (/tmp/backups)]
  --help               Show this message and exit.
```

`$BACKUP_PASSWORD=<string>` (**required**)
- password used to encrypt and secure keystore backups. Keystore backup is encrypted using the `zip` utility's password protection feature.

`$KEYSTORE_DIR=<string>` (**default**: `/root/.ethereum/keystore`)
- container location to retrieve keys from

`$BACKUP_PATH=<string>` (**default**: `/tmp/backups`)
- container location to store encrypted keystore backups. **Note:** Using container `volume/mounts`, keystores can be backed-up to all kinds of storage solutions (e.g. USB drives or auto-synced Google Drive folders)

`$AUTO_BACKUP_KEYSTORE=<boolean>` (**default**: `false`)
- automatically backup keystore to $BACKUP_PATH location every $BACKUP_INTERVAL seconds

`$BACKUP_INTERVAL=<cron-schedule>` (**default**: `0 * * * * (hourly)`)
- keystore backup frequency based on cron schedules


##### Import backup

Decrypt and import backed-up keystore to designated container/host keystore location.

```
$ geth-helper account import-backup --help
Usage: geth-helper account import-backup [OPTIONS] PASSWORD

  Decrypt and import wallet keystores backups.

  PASSWORD password used to decrypt and import keystore backups

Options:
  --keystore-dir TEXT  directory to import a backed-up geth wallet key store
                       [default: (/root/.ethereum/keystore)]
  --backup-path TEXT   path containing backup of a geth wallet key store
                       [default: (/tmp/backups/wallet-backup.zip)]
  --help               Show this message and exit.
```

`$password=<string>` (**required**)
- password used to decrypt keystore backups. Keystore backup is decrypted using the `zip/unzip` utility's password protection feature.

`$KEYSTORE_DIR=<string>` (**default**: `/root/.ethereum/keystore`)
- container location to import keys

`$BACKUP_PATH=<string>` (**default**: `/tmp/backups`)
- container location to retrieve keystore backup. **Note:** Using container `volume/mounts`, keystores can be imported from all kinds of storage solutions (e.g. USB drives or auto-synced Google Drive folders)

##### Query RPC

Execute query against designated `geth` RPC server.

```
$ geth-helper status query-rpc --help
Usage: geth-helper status query-rpc [OPTIONS]

  Execute RPC query

Options:
  --rpc-addr TEXT  server address to query for RPC calls  [default:
                   (http://localhost:8545)]
  --method TEXT    RPC method to execute a part of query  [default:
                   (eth_syncing)]
  --params TEXT    comma separated list of RPC query parameters  [default: ()]
  --help           Show this message and exit.
```

`$RPC_ADDRESS=<web-address>` (**default**: `localhost:8545`)
- `geth` RPC server address for querying network state

`$RPC_METHOD=<geth-rpc-method>` (**default**: `eth_syncing`)
- `geth` RPC method to execute

`$RPC_PARAMS=<rpc-method-params>` (**default**: `''`)
- `geth` RPC method parameters to include within call

The output consists of a JSON blob corresponding to the expected return object for a given RPC method. Reference [Ethereum's RPC API wiki](https://eth.wiki/json-rpc/API) for more details.

###### example

```bash
docker exec --env RPC_ADDRESS=geth-rpc.live.01labs.net --env RPC_METHOD=eth_gasPrice \
    0labs/geth:latest geth-helper status query-rpc

"0xe0d7b70f7" # 60,355,735,799 wei
```

Examples
----------------

* Create account and bind data/keystore directory to host path:
```
docker run -it -v /mnt/geth/data:/root/.ethereum/ 0labs/geth:latest geth account new --password <secret>
```

* Launch an Ethereum light client and connect it to the Ropsten, best current like-for-like representation of Ethereum, PoW (Proof of Work) test network:
```
docker run --env CONFIG-Eth-SyncMode=light 0labs/geth:latest geth --ropsten
```

* View sync progress of active local full-node:
```
docker run --name 01-geth --detach --env CONFIG-Eth-SyncMode=full 0labs/geth:latest geth --mainnet

docker exec 01-geth geth-helper status sync-progress
```

* Run *fast* sync node with automatic daily backups of custom keystore directory:
```
docker run --env CONFIG-Eth-SyncMode=fast --env KEYSTORE_DIR=/tmp/keystore \
           --env AUTO_BACKUP_KEYSTORE=true --env BACKUP_INTERVAL="0 * * * *" \
           --env BACKUP_PASSWORD=<secret> \
  --volume ~/.ethereum/keystore:/tmp/keystore 0labs/geth:latest
```

* Import account from keystore backup stored on an attached USB drive:
```
docker run --name 01-geth --detach --env CONFIG-Eth-SyncMode=full \
           --volume /path/to/usb/mount/keys:/tmp/keys \
           --volume ~/.ethereum:/root/.ethereum \0labs/geth:latest geth --mainnet

docker exec --env BACKUP_PASSWORD=<secret>
            --env BACKUP_PATH=/tmp/keys/my-wallets.zip
            01-geth geth-helper account import-backup

docker exec 01-geth account import /root/.ethereum/keystore/a-wallet
```

License
-------

MIT

Author Information
------------------

This Containerfile was created in 2021 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

* **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

* **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

* **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
