

# :octocat: Geth :cloud: Compose

Custom configuration of this deployment composition can be provided by setting environment variables of the operation environment explicitly:

`export chain=mainnet`

or included within an environment config file located either at a `.env` file within the same directory or specified via the `env_vars` environment variable.

`export env_vars=/home/user/.ethereum/mainnet_vars.env`

## Config


**Required**

`none`

**Optional**

| var | description | default |
| :---: | :---: | :---: |
| image | .... | 0labs/geth:latest |
| chain | .... | rinkeby |

## Deploy environment examples


```

```
