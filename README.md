<p><img src="https://avatars1.githubusercontent.com/u/12563465?s=200&v=4" alt="OCI logo" title="oci" align="left" height="70" /></p>
<p><img src="https://retohercules.com/images/ethereum-png-11.png" alt="ethereum logo" title="ethereum" align="right" height="80" /></p>

Container File :computer: :link: Geth
=========
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/container-file-geth?color=yellow)
[![Build Status](https://travis-ci.org/0x0I/container-file-geth.svg?branch=master)](https://travis-ci.org/0x0I/container-file-geth)
[![Docker Pulls]()](<docker-hub-link)
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
* _install_
* _config_
* _launch_

...

#### Install

...*description of installation related vars*...

#### Config

...*description of configuration related vars*...

#### Launch

...*description of launch related vars*...

Dependencies
------------

None

Example Run
----------------
default example:
```
podman run \
  --env NAME=value \
  0labs/0x01.<service>:<tag> \
```

License
-------

MIT

Author Information
------------------

This Containerfile was created in 2020 by O1.IO.
