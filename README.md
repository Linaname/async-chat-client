# Python-based chat client

Chat client for minechat.dvmn.org

## How to install

```bash
$ pip istall -r requirements.txt
```

## How to use

```bash
$ python minechat_listener.py --help
usage: minechat_listener.py [-h] [--host HOST] [--port PORT] [--history HISTORY]
               [--delay DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           host name or ip address
  --port PORT           port
  --history HISTORY     path to file with history
  --delay DELAY      delay between connect retries

```

You also can set environment variables:

```bash

$ export HOST=minechat.dvmn.org
$ export PORT=5000
$ export DELAY=3
$ export HISTORY=history.txt
$ python minechat_listener.py

```
