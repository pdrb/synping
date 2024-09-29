# synping

[![CI](https://github.com/pdrb/synping/actions/workflows/ci.yml/badge.svg)](https://github.com/pdrb/synping/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/synping.svg)](https://pypi.python.org/pypi/synping)
[![Version](https://img.shields.io/pypi/v/synping.svg)](https://pypi.python.org/pypi/synping)
[![Downloads](https://static.pepy.tech/badge/synping)](https://pepy.tech/project/synping)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![LICENSE](https://img.shields.io/github/license/pdrb/synping)](https://github.com/pdrb/synping/blob/master/LICENSE)

Ping hosts using tcp syn packets.

Please note that full tcp handshake is used, we want the program to behave nicely
and to explicit close the connection after each "ping".

Simple example:
```text
$ synping example.org

Pinging example.org 4 times on port 80:

Reply from 93.184.215.14:80 time=126.17 ms
Reply from 93.184.215.14:80 time=126.54 ms
Reply from 93.184.215.14:80 time=129.27 ms
Reply from 93.184.215.14:80 time=133.44 ms

Statistics:
--------------------------

Host: example.org

Sent: 4 packets
Received: 4 packets
Lost: 0 packets (0.00)%

Min time: 126.17 ms
Max time: 133.44 ms
Average time: 128.85 ms
```

## Notes

* Works on Python 3.6+, for older Python (2.6, 2.7, 3.4...) use synping 0.9
* Uses only standard library for maximum compatibility

## Install

Install using pip:
```shell
pip install synping
```

Or download and set executable permission on the script file:
```shell
chmod +x synping.py
```

Or download and run using the python interpreter:
```shell
python synping.py
```

## Usage

```text
usage: synping host [options]

ping hosts using tcp syn packets

positional arguments:
  host           host to ping

options:
  -h, --help     show this help message and exit
  -t             ping host until stopped with 'control-c'
  -n COUNT       number of requests to send (default: 4)
  -p PORT        port to ping (default: 80)
  -w TIMEOUT     timeout in seconds to wait for reply (default: 3)
  -v, --version  show program's version number and exit

e.g.: synping example.org
```

## Examples

Ping host on port 80 (default):
```shell
synping host
```

Ping host on port 22:
```shell
synping host -p 22
```

Ping host 10 times with 1 second timeout:
```shell
synping host -n 10 -w 1
```
