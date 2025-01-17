# Spotify QR player

Use a webcam to read QR codes and play albums/playlists on Spotify

## Requirements

- Python 3.12+
- zbar


## Setup

### Spotify

Create a new Spotify app:

[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

Make a note of your _Client ID_ and _Client Secret_


## Installation

### macOS

```sh
brew install zbar
```

### Raspberry Pi:

Running this on a Raspberry Pi may involve installing the following:

```
sudo apt update
sudo apt upgrade
sudo apt install -y python3-picamera2
```

You may also need:

```
sudo apt install -y libcamera-apps libcamera-dev python3-libcamera python3-pyzbar python3-numpy python3-pyqt5 libcap-dev libzbar0 libzbar-dev
```


### Python

Create a virtual env:

```sh
python -m venv env
source env/bin/activate
```

On a Raspberry Pi you may need to replace the above with:

```sh
python -m venv --system-site-packages env
```

Install dependencies:

```sh
pip install -r requirements.txt
```

### .env

Duplicate the `.env.example` file, call it `.env` and populate it

```sh
cp .env.example .env
```


## Running

```sh
python main.py
```


## URLs

### Bill Withers - Just As I Am

URL: https://open.spotify.com/album/6N8uPmDqbgXD3ztkCCfxoo

Spotify URL: spotify:album:6N8uPmDqbgXD3ztkCCfxoo

![](./images/album-bill-withers.png)

### Soul playlist

URL: https://open.spotify.com/playlist/5lqpiF52jXxDYwUUeANTbI

Spotify URL: spotify:playlist:5lqpiF52jXxDYwUUeANTbI

![](./images/playlist-soul.png)

---


## Maintenance and support

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

---

## License

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

```
