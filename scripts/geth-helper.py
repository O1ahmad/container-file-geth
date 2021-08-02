#!/usr/bin/env python3

import os
import subprocess

import click
import requests
import toml

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass

@cli.group()
def account():
    pass

@cli.group()
def config():
    pass

@cli.group()
def status():
    pass

###
# Commands for application configuration customization and inspection
###

DEFAULT_GETH_CONFIG_PATH = "/root/.ethereum/geth/config.toml"
DEFAULT_GETH_KEYSTORE_DIR = "/root/.ethereum/keystore"
DEFAULT_GETH_BACKUP_PATH = "/tmp/backups"

def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode > 0:
        print(output.decode('utf-8'))
        print(error.decode('utf-8'))
        print('Executing command \"%s\" returned a non-zero status code %d' % (command, process.returncode))
        sys.exit(process.returncode)

    if error:
        print(error.decode('utf-8'))

    return output.decode('utf-8')

def execute_jsonrpc(rpc_address, method, params):
    req = {
        "jsonrpc":"2.0",
        "method":method,
        "params":params,
        "id":1
    }

    h = {'Content-Type': 'application/json'}
    result = requests.post(rpc_address, data=req, headers=h)
    import pdb; pdb.set_trace()

@config.command()
@click.option('--config-path',
              default=DEFAULT_GETH_CONFIG_PATH,
              help='path to geth configuration file to generate or customize from environment config settings')
def customize(config_path):
    config_dict = dict()
    if os.path.isfile(config_path):
        config_dict = toml.load(config_path)

    for var in os.environ.keys():
        var_split = var.split('_')
        if len(var_split) == 3 and var_split[0].lower() == "config":
	    # support encoding of '.' or dot char within config settings
            # with 'dot' (e.g. "CONFIG_Node.P2P_MaxPeers" should be represented
            # as "CONFIG_NodedotP2P_MaxPeers"
            config_section = var_split[1].replace("dot", ".")
            section_setting = var_split[2]

            if config_section not in config_dict:
                config_dict[config_section] = {}

            value = os.environ[var]
            if value.isdigit():
                value = int(value)
            config_dict[config_section][section_setting] = value

    with open(config_path, 'w+') as f:
        toml.dump(config_dict, f)

    # TODO: determine better workaround for toml double-quotation parsing re: section names and list
    # technically, the python toml parser should be better/smarter about handling these cases

    # remove surrounding quotes from ALL section names if necessary
    subprocess.call(["sed -i 's/\[\"/\[/g' {path}".format(path=config_path)], shell=True)
    subprocess.call(["sed -i 's/\"\]/\]/g' {path}".format(path=config_path)], shell=True)
    # remove surrounding quotes from ALL list setting values if necessary
    subprocess.call(["sed -i 's/\"\[/\[/g' {path}".format(path=config_path)], shell=True)
    subprocess.call(["sed -i 's/\]\"/\]/g' {path}".format(path=config_path)], shell=True)

@account.command()
@click.argument('password')
@click.option('--keystore-dir',
              default=DEFAULT_GETH_KEYSTORE_DIR,
              help='path to geth wallet key store')
@click.option('--backup-path',
              default=DEFAULT_GETH_BACKUP_PATH,
              help='path to backup geth wallet key stores')
def backup_keystore(password, keystore_dir, backup_path):
    """Encrypt and backup wallet keystores.

    PASSWORD password used to encrypt and secure keystore backups.
    """

    subprocess.call(
        [
            "cd {keystore} && zip --password {pwd} {backup} *".format(
                backup=backup_path,
                keystore=keystore_dir,
                pwd=password
            )
        ],
        shell=True)

@account.command()
@click.argument('password')
@click.option('--keystore-dir',
              default=DEFAULT_GETH_KEYSTORE_DIR,
              help='path to import a backed-up geth wallet key store')
@click.option('--backup-path',
              default=DEFAULT_GETH_BACKUP_PATH,
              help='path containing backup of a geth wallet key store')
def import_backup(password, keystore_dir, backup_path):
    """Decrypt and import wallet keystores backups.

    PASSWORD password used to decrypt and import keystore backups.
    """

    rc = subprocess.call(
        [
            "unzip -P {pwd} -d {keystore} {backup}".format(
                backup=backup_path,
                keystore=keystore_dir,
                pwd=password
            )
        ],
        shell=True)
    if rc != 0:
        print("Import of keystore backup [{backup}] failed with exit code: {code}.".format(backup=backup_path, code=rc))

@status.command()
@click.option('--data-dir',
              default=DEFAULT_GETH_DATADIR,
              help='path to geth data directoty')
def check_balances(datadir):
    """Check all stored account balances.
    """

    rc = execute_jsonrpc(
        "https://mainnet.infura.io/v3/4a3a6c645dc94d1b82f8f631a878e03c",
        "eth_getBalance",
        params=["0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c","latest"])
    print(rc)
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    cli()
