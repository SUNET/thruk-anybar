# thruk-anybar
Show a general status from [Thruk](https://www.thruk.org) in [AnyBar](https://github.com/tonsky/AnyBar).

Patches are welcome!

![Screenshot](https://raw.githubusercontent.com/SUNET/thruk-anybar/main/sample/thruk-anybar.png)


## Prerequisites

* Install Anybar
```
brew install anybar
```
* Depending of python version you might need some modules (this is the system wide python)
```
/usr/bin/python3 -m pip install psutil toml requests
```

## Installation
* Run `./INSTALLER`
* Create/edit `~/.Anybar/thruk-anybar.toml` (see example below)
* Create (or copy from `icons/`) icons for your sites to `~/.Anybar`. Naming schema `SITE-COLOR@2x.png` (read more about colors below)


## Configuration
Configuration is done via `~/.Anybar/thruk-anybar.toml`, a simple TOML file. Each site get it's own table. Increse port number for each site. The site name (table name) must be named as the icons.
The API key can be created in Thruk under User Profile. E.g https://monitor.example.com/thruk/cgi-bin/user.cgi#apikeys
```
[swamid]
baseurl = "https://monitor.swamid.se"
key = "REDACTED"
port = 1738

[mastodon]
baseurl = "https://monitor.social.sunet.se"
key = "REDACTED"
port = 1739

[geteduroam]
baseurl = "https://monitor.geteduroam.sunet.se"
key = "REDACTED"
port = 1740
```

## Colors of icon

|Color|Status|
| --- | --- |
|Green|Everything is OK in the monitor|
|Red|Attention is needed|
|Yellow|`thruk-anybar.py` is in vacation mode|
|Black|Connection error or not yet run|
|Purple|thruk didn't respond with a proper json, server error?|
