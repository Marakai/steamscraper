#!/usr/bin/env python3

import argparse
from steamscraper import SteamScraper, __version__


def args_handler():
    argparser = argparse.ArgumentParser(prog='steamscraper', formatter_class=argparse.RawTextHelpFormatter, description=
    '''
    Grab subscribed workshop addons from Steam Workshop (default is to grab them for Ark Survival Evolved).

    Authenticates to Steam Store with 2FA (only, for now) then looks for all the subscribed addons, 
    extracting name and addon ID.
    ''')
    argparser.add_argument('-v', '--version', action='version',
                           version=f'%(prog)s {__version__}')
    argparser.add_argument('--username',
                           help='Steam user name',
                           required=True)
    argparser.add_argument('--password',
                           help='Password',
                           required=False)
    argparser.add_argument('--mfatoken',
                           help='2FA token value',
                           required=False)
    argparser.add_argument('--prompt',
                           help='Prompt for authentication info',
                           required=False, default=False, action='store_true')
    argparser.add_argument('--appid',
                           help='The Steam Workshop App ID, which you need to figure out. Default is 346110 for Ark Survival Evolved',
                           required=False, default='346110')
    argparser.add_argument('--arkmanager',
                           help='Issue list in Arkmanager instance config format',
                           required=False, default=False, action='store_true')
    args = argparser.parse_args()
    return args, argparser


def main():
    args, ap = args_handler()
    if args.prompt:
        steam = SteamScraper(username=args.username, prompt=True, appid=args.appid)
    else:
        steam = SteamScraper(username=args.username, pw=args.password, mfa=args.mfatoken, appid=args.appid)
    res = steam.get_data()
    for k, v in res.items():
        if args.arkmanager:
            print(f'# "{v}" is {k}')
            print(f'arkmod_{k}=game')
        else:
            print(f'{v},{k}')


if __name__ == '__main__':
    main()
