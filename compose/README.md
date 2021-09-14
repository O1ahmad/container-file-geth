# Geth :cloud: Compose

:octocat: Custom configuration of this deployment composition can be provided by setting environment variables of the operation environment explicitly:

`export chain=mainnet`

or included within an environment config file located either at a `.env` file within the same directory or specified via the `env_vars` environment variable.

`export env_vars=/home/user/.ethereum/mainnet_vars.env`

## Config


**Required**

`none`

**Optional**

| var | description | default |
| :---: | :---: | :---: |
| *image* | Geth service container image to deploy | `0labs/geth:latest` |
| *chain* | Ethereum network/chain to connect geth instance to | `rinkeby` |
| *GETH_CONFIG_DIR* | configuration directory path within container | `/etc/geth` |
| *p2p_port* | Peer-to-peer network discovery and communication listening port | `30303` |
| *rpc_port* | HTTP-RPC server listening portport | `8545` |
| *websocket_port* | WS-RPC server listening port | `8546` |
| *metrics_port* | Metrics HTTP server listening port | `6060` |
| *metrics_addr* | Enable stand-alone metrics HTTP server listening interface | `127.0.0.1` |
| *env_vars* | Path to environment file to load by compose Geth container | `.env` |
| *host_data_dir* | Host directory to store client runtime/operational data | `/var/tmp/geth` |
| *restart_policy* | container restart policy | `unless-stopped` |
| *exporter_image* | Geth data exporter image to deploy | `hunterlong/gethexporter:latest` |
| *exporter_rpc_addr* | Network address <ip:port> of geth rpc instance to export data from | `http://localhost:8545` |
| *exporter_port* | Exporter metrics collection listening port | `10090` |

## Deploy examples

* Launch an Ethereum light client and connect it to the Ropsten, best current like-for-like representation of Ethereum, PoW (Proof of Work) test network:
```
# cat .env
chain=ropsten
CONFIG-Eth-SyncMode=light

docker-compose up
```

* View sync progress of active local full-node:
```
# cat .env
chain=mainnet
CONFIG-Eth-SyncMode=full

docker-compose up -d  && docker-compose exec geth geth-helper status sync-progress
```

* Run *fast* sync node with automatic daily backups of custom keystore directory:
```
# cat .env
chain=mainnet
CONFIG-Eth-SyncMode=fast
KEYSTORE_DIR=/tmp/keystore
AUTO_BACKUP_KEYSTORE=true
BACKUP_INTERVAL='0 * * * *'
BACKUP_PASSWORD=<secret>

docker-compose up
```

* Customize Geth deploy image and p2p port
```
# cat .env
image=0labs/geth:v0.1.0
p2p_port=30313

docker-compose up
```

* Import account from keystore backup stored on an attached USB drive:
```
# cat .env
host_data_dir=/tmp/geth
BACKUP_PASSWORD=<secret>
BACKUP_PATH=/tmp/geth/keys/my-wallets.zip

docker-compose up -d

cp /path/to/usb/my-wallets.zip /tmp/geth/keys
docker-compose exec geth geth-helper account import-backup

docker-compose exec geth geth account import /root/.ethereum/keystore/a-wallet
```
