<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ethereum-icon-purple.svg/1200px-Ethereum-icon-purple.svg.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![Build Status](https://travis-ci.org/0x0I/container-file-geth.svg?branch=master)](https://travis-ci.org/0x0I/container-file-geth)
[![Docker Pulls](https://img.shields.io/docker/pulls/0labs/0x01.geth?style=flat)](https://hub.docker.com/repository/docker/0labs/0x01.geth)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

**Table of Contents**
  - [Environment Variables](#environment-variables)
      - [Config](#config)
      - [Launch](#launch)
      - [Operations](#operations)
  - [Example Run](#example-run)
  - [License](#license)
  - [Author Information](#author-information)

Container file that configures and runs [Geth](https://geth.ethereum.org): a command-line interface and API server for operating an Ethereum node.

Environment Variables
--------------
Variables are available and organized according to the following software & machine provisioning stages:
* _config_
* _launch_

#### Config

Configuration of the `geth` client can be expressed in a config file written in [TOML](https://github.com/toml-lang/toml), a minimal markup language, used as an alternative to passing command-line flags at runtime. To get an idea how the config should look you can use the `geth dumpconfig` subcommand to export a client's existing configuration.

_The following variables can be customized to manage the content of this TOML configuration:_
 
`$CONFIG_<section-keyword>_<section-property> = <property-value (string)>` **default**: *None*

* Any configuration setting/value key-pair supported by `geth` should be expressible within each `CONFIG_*` environment variable and properly rendered within the associated TOML config. **Note:** `<section-keyword>` along with the other property specifications should be written as expected to be rendered within the associated `TOML` config (**e.g.** *Node.P2P*).

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

...

Example Run
----------------
Basic setup with defaults:
```
docker run 0labs/geth
```

Launch an Ethereum light client and connect it to the Rinkeby PoA (Proof of Authority) test network:
```
docker run --env CONFIG_Eth_SyncMode='"light"' 0labs/geth --rinkeby
```

Run a full Ethereum node using "fast" sync-mode (only process most recent transactions), enabling both the RPC server interface and overriding the (block) data directory:
```
docker run --env CONFIG_Eth_SyncMode='"fast"' \
           --env CONFIG_Node_DataDir='"/mnt/geth/data"' \
           --volume geth_data:/mnt/geth/data
           0labs/geth --rpc
```

License
-------

MIT

Author Information
------------------

This Container file was created in 2020 by O1.IO.
