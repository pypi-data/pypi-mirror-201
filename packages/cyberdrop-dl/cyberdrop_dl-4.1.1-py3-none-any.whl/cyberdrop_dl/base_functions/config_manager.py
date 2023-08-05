from __future__ import annotations

import copy
from pathlib import Path

import yaml

from cyberdrop_dl.base_functions.base_functions import log
from cyberdrop_dl.base_functions.config_schema import config_default


def _to_config_value(value):
    return str(value) if isinstance(value, Path) else value


def _create_config(config: Path, passed_args: dict = None, enabled=False) -> dict:
    """Creates the default config file, or remakes it with passed arguments"""
    config_data = config_default
    if passed_args:
        config_data["Apply_Config"] = enabled
        for group in config_data["Configuration"].values():
            for arg in group:
                if arg in passed_args:
                    group[arg] = _to_config_value(passed_args[arg])

    with open(config, 'w') as yamlfile:
        yaml.dump(config_data, yamlfile)

    return config_data


def _validate_config(config: Path) -> dict:
    """Validates the existing config file"""
    with open(config, "r") as yamlfile:
        config_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    try:
        data = config_data["Configuration"]
        enabled = config_data["Apply_Config"]

        config_groups = config_default["Configuration"]
        if all(set(group) <= set(data[group_name]) for group_name, group in config_groups.items()):
            return config_data

        config.unlink()

        args = {}
        for group_name in config_groups:
            args.update(data[group_name])
        config_data = _create_config(config, args, enabled)

    except (KeyError, TypeError):
        config.unlink()
        config_data = _create_config(config)

    return config_data


def run_args(config: Path, cmd_arg: dict) -> dict:
    """Returns the proper runtime arguments based on the config and command line arguments"""
    data = _validate_config(config) if config.is_file() else _create_config(config, cmd_arg)
    if data['Apply_Config']:
        data = data["Configuration"]
        for file, path in data['Files'].items():
            data['Files'][file] = Path(path)
        data['Sorting']['sort_directory'] = Path(data['Sorting']['sort_directory'])
        return data

    config_data = config_default["Configuration"]
    for group in config_data.values():
        for arg in group:
            if arg in cmd_arg:
                group[arg] = cmd_arg[arg]
    return config_data


async def document_args(args: dict):
    """We document the runtime arguments for debugging and troubleshooting, redacting sensitive information"""
    print_args = copy.deepcopy(args)
    print_args['Authentication']['xbunker_password'] = '!REDACTED!' if args['Authentication']['xbunker_password'] is not None else None
    print_args['Authentication']['socialmediagirls_password'] = '!REDACTED!' if args['Authentication']['socialmediagirls_password'] is not None else None
    print_args['Authentication']['simpcity_password'] = '!REDACTED!' if args['Authentication']['simpcity_password'] is not None else None
    print_args['Authentication']['pixeldrain_api_key'] = '!REDACTED!' if args['Authentication']['pixeldrain_api_key'] is not None else None
    print_args['JDownloader']['jdownloader_password'] = '!REDACTED!' if args['JDownloader']['jdownloader_password'] is not None else None

    await log("Starting Cyberdrop-DL")
    await log(f"Using authentication arguments: {print_args['Authentication']}", quiet=True)
    await log(f"Using file arguments: {print_args['Files']}", quiet=True)
    await log(f"Using forum option arguments: {print_args['Forum_Options']}", quiet=True)
    await log(f"Using ignore arguments: {print_args['Ignore']}", quiet=True)
    await log(f"Using jdownloader arguments: {print_args['JDownloader']}", quiet=True)
    await log(f"Using progress option arguments: {print_args['Progress_Options']}", quiet=True)
    await log(f"Using ratelimiting arguments: {print_args['Ratelimiting']}", quiet=True)
    await log(f"Using runtime arguments: {print_args['Runtime']}", quiet=True)
    await log(f"Using sorting arguments: {print_args['Sorting']}", quiet=True)
