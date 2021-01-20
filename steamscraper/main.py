#!/usr/bin/env python3

import argparse

# usual brain damage when running from inside Pycharm
try:
    from steamscraper.steamscraper import SteamScraper
    from steamscraper import version
except:
    from steamscraper import SteamScraper
    import version


def args_handler():
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=
    '''
        Grab subscribed workshop addons from Steam for Ark Survival Evolved.

        Authenticates to Steam Store with 2FA (only, for now), with Ark Survival app ID, then
        looks for all the subscribed addons, extracting name and addon ID.
        ''')
    argparser.add_argument('-v', '--version', action='version',
                           version='%(prog)s {version}'.format(version=version.__version__))
    argparser.add_argument('--username',
                           help='Steam user name',
                           required=True)
    argparser.add_argument('--password',
                           help='Password',
                           required=False)
    argparser.add_argument('--mfatoken',
                           help='2FA token valyue',
                           required=False)
    argparser.add_argument('--prompt',
                           help='Prompt for authentication info',
                           required=False, default=False, action='store_true')
    args = argparser.parse_args()
    return args, argparser


def main():
    args, ap = args_handler()
    if args.prompt:
        steam = SteamScraper(username=args.username, prompt=True)
    else:
        steam = SteamScraper(username=args.username, pw=args.password, mfa=args.mfatoken)
    res = steam.get_data()
    for k, v in res.items():
        print(f'{v},{k}')


if __name__ == '__main__':
    main()
