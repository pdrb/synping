|Downloads|

synping
=======

Ping hosts using tcp syn packets.

Please note that full tcp handshake is used, we want the program to behave nicely
and to explicit close the connection after each "ping".

Simple example::

    $ synping example.org

    Pinging example.org 4 times on port 80:

    Reply from 93.184.216.34:80 time=7.40 ms
    Reply from 93.184.216.34:80 time=10.31 ms
    Reply from 93.184.216.34:80 time=7.18 ms
    Reply from 93.184.216.34:80 time=6.92 ms

    Statistics:
    --------------------------

    Host: example.org

    Sent: 4 packets
    Received: 4 packets
    Lost: 0 packets (0.00%)

    Min time: 6.92 ms
    Max time: 10.31 ms
    Average time: 7.95 ms


Notes
=====

- Works on Python 2 and Python 3
- Uses only Python standard library for maximum compatibility


Install
=======

Install using pip::

    pip install synping

or

Download and set executable permission on the script file::

    chmod +x synping.py

or

Download and run using the python interpreter::

    python synping.py


Usage
=====

::

    Usage: synping host [options]

    ping hosts using tcp syn packets

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -t          ping host until stopped with 'control-c'
      -n COUNT    number of requests to send (default: 4)
      -p PORT     port number to use (default: 80)
      -w TIMEOUT  timeout in seconds to wait for reply
                  (default: 3)


Examples
========

Ping host on port 80 (default)::

    $ synping host

Ping host on port 22::

    $ synping host -p 22

Ping host 10 times with 1 second timeout::

    $ synping host -n 10 -w 1


.. |Downloads| image:: https://pepy.tech/badge/synping
