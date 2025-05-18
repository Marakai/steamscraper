### Steamscraper

Quick and dirty tool that used the Steam API/SDK for Python to extract all subscribed mods for
a given App ID from the Steam Workshop.

The default app ID is for Ark Survival Evolved which this was originally written for. I have not done much
testing for other apps!

#### Usage

```
usage: steamscraper [-h] [-v] [--config CONFIG] [--appid APPID] [--arkmanager]

    Grab subscribed workshop addons from Steam Workshop (default is to grab them for Ark Survival Evolved).

    Authenticates to Steam Store with 2FA (only, for now) then looks for all the subscribed addons, 
    extracting name and addon ID.


optional arguments:
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
  --config CONFIG      Path to the configuration file (default: steam-credentials.conf)
  --arkmanager         Issue list in Arkmanager instance config format
```

#### Build and Installation

1. Clone Repo
2. If you have `make` installed
   - `make wheel`; or if you're brave
   - `make install` (will install into --user)
3. If you don't have `make`, inspect the `Makefile` to run the individual steps from init->wheel->install

#### Testing

`make tests`

or run the command under that target in the `Makefile`

#### Configuration

The configuration file uses TOML.

```toml
# Steam credentials configuration file

# Steam Workshop App ID (default is 346110 for Ark Survival Evolved)
appid = "123456"

# Steam user ID (mandatory)
steamlogin = "mylogin"

# Steam username (mandatory)
username = "myusername"

# Steam password (mandatory)
password = "mypassword"

# Steam ID (mandatory)
steamid = "mysteamid"
```