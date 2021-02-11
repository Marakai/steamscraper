### Steamscraper

Quick and dirty tool that used the Steam API/SDK for Python to extract all subscribed mods for
a given App ID from the Steam Workshop.

The default app ID is for Ark Survival Evolved which this was originally written for. I have not done much
testing for other apps!

#### Usage

```
usage: steamscraper [-h] [-v] --username USERNAME [--password PASSWORD]
                    [--mfatoken MFATOKEN] [--prompt] [--appid APPID]
                    [--arkmanager]

    Grab subscribed workshop addons from Steam Workshop (default is to grab them for Ark Survival Evolved).

    Authenticates to Steam Store with 2FA (only, for now) then looks for all the subscribed addons, 
    extracting name and addon ID.
    

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
  --username USERNAME  Steam user name
  --password PASSWORD  Password
  --mfatoken MFATOKEN  2FA token valyue
  --prompt             Prompt for authentication info
  --appid APPID        The Steam Workshop App ID, which you need to figure out. Default is 346110 for Ark Survival Evolved
  --arkmanager         Issue list in Arkmanager instance config format
```

#### Build and Installation

1. Clone Repo
2. Build source dist with `python3 setup.py sdist`
3. Install with `pip3 install dist/<name of created tarball>`
