# Python-based chat client

Chat client for minechat.dvmn.org

## How to install

```bash
$ pip install -r requirements.txt
```
Python 3.7 is required.

## How to use

### Read messages

Read chat messages and save to file:

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

### Send message

Autorise or register new user by nickname and send message to chat:

```bash
$ python minechat_sender.py -h
usage: minechat_sender.py [-h] [--host HOST] [--port PORT]
                          (--token TOKEN | --nickname NICKNAME) --message
                          MESSAGE

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          host name or ip address
  --port PORT          port
  --token TOKEN        token
  --nickname NICKNAME  nickname
  --message MESSAGE    message text
```
