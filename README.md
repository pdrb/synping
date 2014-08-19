#synping

Python script to "ping" hosts using tcp syn packets.

##Install

Download and set executable permission on the script file:
>chmod +x synping.py

Alternatively you can run using the python interpreter:
>python synping.py

###Usage

>$ ./synping.py HOST [port] [count]

####Examples:

Ping localhost indefinitely on a random port:
>$ ./synping.py localhost

Ping localhost indefinitely on port 80:
>$ ./synping.py localhost 80

Ping localhost 10 times on port 80
>$ ./synping.py localhost 80 10
