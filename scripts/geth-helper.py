#!/usr/bin/env python3

from datetime import datetime
import json
import os
import subprocess
import sys

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
DEFAULT_GETH_DATADIR = "/root/.ethereum"
DEFAULT_GETH_KEYSTORE_DIR = "/root/.ethereum/keystore"
DEFAULT_GETH_BACKUP_PATH = "/tmp/backups/wallet-backup.zip"

DEFAULT_RPC_ADDRESS = "http://localhost:8545"
DEFAULT_RPC_METHOD = "eth_syncing"
DEFAULT_RPC_PARAMS = ""

def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode > 0:
        print('Executing command \"%s\" returned a non-zero status code %d' % (command, process.returncode))
        sys.exit(process.returncode)

    if error:
        print(error.decode('utf-8'))

    return output.decode('utf-8')

def execute_jsonrpc(rpc_address, method, params):
    req = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    result = requests.post(rpc_address, json=req, headers={'Content-Type': 'application/json'})
    if result.status_code == requests.codes.ok:
        return result
    else:
        result.raise_for_status()

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
              default=lambda: os.environ.get("KEYSTORE_DIR", DEFAULT_GETH_KEYSTORE_DIR),
              show_default=DEFAULT_GETH_KEYSTORE_DIR,
              help='geth wallet key store directory to backup')
@click.option('--backup-path',
              default=lambda: os.environ.get("BACKUP_PATH", DEFAULT_GETH_BACKUP_PATH),
              show_default=DEFAULT_GETH_BACKUP_PATH,
              help='path to create geth wallet key store backup at')
def backup_keystore(password, keystore_dir, backup_path):
    """Encrypt and backup wallet keystores.

    PASSWORD password used to encrypt and secure keystore backups
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
              default=lambda: os.environ.get("KEYSTORE_DIR", DEFAULT_GETH_KEYSTORE_DIR),
              show_default=DEFAULT_GETH_KEYSTORE_DIR,
              help='directory to import a backed-up geth wallet key store')
@click.option('--backup-path',
              default=lambda: os.environ.get("BACKUP_PATH", DEFAULT_GETH_BACKUP_PATH),
              show_default=DEFAULT_GETH_BACKUP_PATH,
              help='path containing backup of a geth wallet key store')
def import_backup(password, keystore_dir, backup_path):
    """Decrypt and import wallet keystores backups.

    PASSWORD password used to decrypt and import keystore backups
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
@click.option('--rpc-addr',
              default=lambda: os.environ.get("RPC_ADDRESS", DEFAULT_RPC_ADDRESS),
              show_default=DEFAULT_RPC_ADDRESS,
              help='server address to query for RPC calls')
def check_balances(rpc_addr):
    """Check all client managed account balances
    """

    # collect addresses managed by client
    result = []
    accounts = execute_jsonrpc(
        rpc_addr,
        "eth_accounts",
        params=[]).json()['result']
    for acct in accounts:
        balance = execute_jsonrpc(
            rpc_addr,
            "eth_getBalance",
            params=[acct,"latest"]).json()['result']
        result.append({ "account": acct, "balance": int(balance, 16) })

    print(json.dumps(result))

@status.command()
@click.option('--rpc-addr',
              default=lambda: os.environ.get("RPC_ADDRESS", DEFAULT_RPC_ADDRESS),
              show_default=DEFAULT_RPC_ADDRESS,
              help='server address to query for RPC calls')
def sync_progress(rpc_addr):
    """Check client blockchain sync status and process
    """

    status = execute_jsonrpc(
        rpc_addr,
        "eth_syncing",
        params=[]).json()['result']

    if status != False:
        lastPercentage = 0; lastBlocksToGo = 0; timeInterval = 0
        date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        syncPath = '/tmp/geth-sync-progress.json'
        if os.path.isfile(syncPath):
            with open(syncPath, 'r') as sync_file:
                data = json.load(sync_file)
                lastPercentage = data['lastPercentage']
                lastBlocksToGo = data['lastBlocksToGo']

                lastSyncTime = datetime.strptime(data['time'], date_format_str)
                timeInterval = (datetime.now() - lastSyncTime).total_seconds()

        percentage = (int(status['currentBlock'], 16) / int(status['highestBlock'], 16)) * 100
        percentagePerTime = percentage - lastPercentage
        blocksToGo = int(status['highestBlock'], 16) - int(status['currentBlock'], 16)
        bps = 0 if (timeInterval == 0 or lastBlocksToGo == 0) else ((lastBlocksToGo - blocksToGo) / timeInterval)
        etas = 0 if bps == 0 else (blocksToGo / bps)
        etaHours = etas / 3600
        stateProgress = 0 if int(status['knownStates'], 16) == 0 else (int(status['pulledStates'], 16) / int(status['knownStates'], 16)) * 100

        result = {
            "progress": percentage,
            "blocksToGo": blocksToGo,
            "bps": bps,
            "percentageIncrease": percentagePerTime,
            "stateProgress": stateProgress,
            "etaHours": etaHours
        }
        print(json.dumps(result))

        # write out historical data for reference on next invokation
        last_sync_data = {
            "lastPercentage": percentage,
            "lastBlocksToGo": blocksToGo,
            "time": datetime.now().strftime(date_format_str)
        }
        with open(syncPath, 'w') as sync_file:
            json.dump(last_sync_data, sync_file)
    else:
        print(json.dumps({ "progress": "synced" }))

@status.command()
@click.option('--rpc-addr',
              default=lambda: os.environ.get("RPC_ADDRESS", DEFAULT_RPC_ADDRESS),
              show_default=DEFAULT_RPC_ADDRESS,
              help='server address to query for RPC calls')
@click.option('--method',
              default=lambda: os.environ.get("RPC_METHOD", DEFAULT_RPC_METHOD),
              show_default=DEFAULT_RPC_METHOD,
              help='RPC method to execute a part of query')
@click.option('--params',
              default=lambda: os.environ.get("RPC_PARAMS", DEFAULT_RPC_PARAMS),
              show_default=DEFAULT_RPC_PARAMS,
              help='comma separated list of RPC query parameters')
def query_rpc(rpc_addr, method, params):
    """Execute RPC query
    """

    result = execute_jsonrpc(
        rpc_addr,
        method,
        params=[] if len(params) == 0 else params.split(',')
    ).json()['result']

    print(json.dumps(result))

if __name__ == "__main__":
    cli()
