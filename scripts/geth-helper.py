#!/usr/bin/env python3

import os

import click
import toml

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.group()
def config():
    pass


@cli.group()
def account():
    pass

###
# Commands for application configuration customization and inspection
###


DEFAULT_GETH_CONFIG_PATH = "/root/.ethereum/geth/config.toml"


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

@config.command()
@click.option('--config-path',
              default=DEFAULT_GETH_CONFIG_PATH,
              help='path to geth configuration file to generate or customize from environment config settings')
def customize():
    config_dict = dict()
    if os.path.isfile(config_path):
        config_dict = toml.load(config_path)

    for var in os.environ.keys():
        var_split = var.split('_')
        if len(var_split) == 3 and var_split[0].lower() == "config":
            config_section = var_split[1]
            section_setting = var_split[2]

            if config_section not in config_dict:
                config_dict[config_section] = {}
            
            config_dict[config_section][section_setting] = os.environ[var]

    with open(config_path, 'w+') as f:
        toml.dump(config_dict, f)


if __name__ == "__main__":
    cli()