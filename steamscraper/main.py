#!/usr/bin/env python3

import argparse
from steamscraper.steamapi import SteamScraper
from steamscraper.config import SteamConfig
from importlib.metadata import version as get_version

try:
    __version__ = get_version("steamscraper")
except Exception:
    __version__ = "unknown"


def args_handler():
    argparser = argparse.ArgumentParser(prog='steamscraper', formatter_class=argparse.RawTextHelpFormatter, description=
    '''
    Grab subscribed workshop addons from Steam Workshop (default is to grab them for Ark Survival Evolved).

    Authenticates to Steam Store with 2FA (only, for now) then looks for all the subscribed addons, 
    extracting name and addon ID.
    ''')
    argparser.add_argument('-v', '--version', action='version',
                           version=f'%(prog)s {__version__}')
    argparser.add_argument('--config',
                           help='Path to the configuration file (default: steam-credentials.conf)',
                           required=False, default='steam-credentials.conf')
    argparser.add_argument('--arkmanager',
                           help='Issue list in Arkmanager instance config format',
                           required=False, default=False, action='store_true')
    args = argparser.parse_args()
    return args, argparser


def main():
    args, _ = args_handler()
    try:
        config = SteamConfig(config_file=args.config)
        steam = SteamScraper(config=config)
        res = steam.subscription_data()
        for k, v in res.items():
            if args.arkmanager:
                print(f'# "{v}" is {k}')
                print(f'arkmod_{k}=game')
            else:
                print(f'{v},{k}')
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
