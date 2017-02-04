synping
=======

Python script to "ping" hosts using tcp syn packets.

Install
-------

Install using pip:

::

    pip install synping

or

Download and set executable permission on the script file:

::

    chmod +x synping.py

or

Download and run using the python interpreter:

::

    python synping.py

Usage
-----

Similar to "ping" utility:

::

    Usage: synping.py host [options]

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
--------

Ping host on port 80 (default):

::

    $ synping host

Ping host on port 22:

::

    $ synping host -p 22

Ping host 10 times with 1 second timeout:

::

    $ synping host -n 10 -w 1

Notes
-----

- Works on Python 2
- Works fine on Linux and should work on all platforms
- Briefly tested on Windows, Cygwin and OSX
