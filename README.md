# thruk-anybar
Show a general status from thruk in Anybar

Patches are welcome!


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
```
[swamid]
baseurl = "https://monitor.swamid.se"
key = "REDUCTED"
port = 1738

[mastodon]
baseurl = "https://monitor.social.sunet.se"
key = "REDUCTED"
port = 1739

[geteduroam]
baseurl = "https://monitor.geteduroam.sunet.se"
key = "REDUCTED"
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
