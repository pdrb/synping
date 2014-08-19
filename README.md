#synping

Python script to "ping" hosts using tcp syn packets.

##Usage

>$ ./synping.py HOST [port] [count]

###Examples:

Ping localhost indefinitely on a random port:
>$ ./synping localhost

Ping localhost indefinitely on port 80:
>$ ./synping localhost 80

Ping localhost 10 times on port 80
>$ ./synping localhost 80 10
