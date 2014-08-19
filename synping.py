#!/usr/bin/python

# synping v0.1
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 14/06/2014

import socket
import random
import time
import sys

# Set the timeout for the socket
timeout = 3
# Store the packets latency
times = []


# Function to ping the server
def ping(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    t0 = time.time()
    s.connect((host, port))
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    t1 = time.time()
    tt = float(t1 - t0)
    times.append(tt)
    print 'Reply from %s:%d time=%.2f ms' % (host, port, tt * 1000)


# Main function
def main():
    # Check the number of args, do the validation and processing needed
    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print '\nUsage: synping.py <host> [port] [count]\n\nExamples:\n\n' \
              './synping localhost -> Ping localhost indefinitely on a random port\n' \
              './synping localhost 80 -> Ping localhost indefinitely on port 80\n' \
              './synping localhost 80 10 -> Ping localhost 10 times on port 80\n'
        sys.exit(0)
    if len(sys.argv) == 2:
        port = random.randint(1, 65535)
        count = 0
    if len(sys.argv) == 3:
        count = 0
        try:
            port = int(sys.argv[2])
        except:
            print '\nError: Port be an integer.\n'
            sys.exit(0)
    if len(sys.argv) == 4:
        try:
            port = int(sys.argv[2])
            count = int(sys.argv[3])
        except:
            print '\nError: Port and count must be an integer.\n'
            sys.exit(0)
        if count <= 0:
            print '\nError: Count must be a positive number.\n'
            sys.exit(0)
    if port <= 0 or port > 65535:
        print '\nError: Port must be a number between 1 and 65535.\n'
        sys.exit(0)
    host = sys.argv[1]

    # Get the Host IP
    try:
        remote_ip = socket.gethostbyname(host)
    except Exception as ex:
        if 'not know' in str(ex):
            print '\nUNKNOWN host.\n'
        else:
            print ex
        sys.exit(0)

    # Initiate the variables needed for the summary
    rcvd = 0
    sent = 0
    total = 0

    # Print the appropriate beginning message
    if len(sys.argv) == 2:
        print '\nPinging %s indefinitely on a random port:\n' % host
    if len(sys.argv) == 3:
        print '\nPinging %s indefinitely on port %d:\n' % (host, port)
    if len(sys.argv) == 4:
        print '\nPinging %s %d times on port %d:\n' % (host, count, port)

    # Begin the pinging
    try:
        while True:
            # Sleep between the requests
            time.sleep(1)
            # Check the count variable to determine the loop ending
            if count != 0:
                if sent == count:
                    break
            tr0 = time.time()
            try:
                ping(remote_ip, port)
                sent += 1
                rcvd += 1
            except Exception as ex:
                tr1 = time.time()
                # If the host respond with a refused message it means it is alive
                if 'refused' in str(ex):
                    sent += 1
                    rcvd += 1
                    ttr = float(tr1 - tr0)
                    times.append(ttr)
                    print 'Reply from %s:%d time=%.2f ms' % (remote_ip, port, ttr * 1000)
                elif 'timed out' in str(ex):
                    sent += 1
                    print 'Timed out after ' + str(timeout) + ' seconds'
                elif 'argument' in str(ex):
                    print 'INVALID host.\n'
                    sys.exit(0)
                else:
                    sent += 1
                    print ex
    # Catch the keyboard interrupt to end the loop
    except KeyboardInterrupt:
        print '\nAborted.'

    # If no packets received or sent end the program
    if rcvd == 0 or sent == 0:
        print "\nDidn't receive any packets..."
        print "\nHost is probably DOWN or firewalled. Sorry :'(\n"
        sys.exit(0)

    # Calculate the average time
    for i in range(len(times)):
        total += times[i]
    average = total / rcvd

    # Print the summary
    print '\nSummary:'
    print '-' * 26
    print '\nHost: %s\n' % host
    print 'Sent: %d packets\nReceived: %d packets\nLost: %d packets (%.2f%%)\n' \
          % (sent, rcvd, sent - rcvd, float(sent - rcvd) / sent * 100)
    print 'Min time: %.2f ms\nMax time: %.2f ms\nAverage time: %.2f ms\n' \
          % (min(times) * 1000, max(times) * 1000, average * 1000)

# Program begins here
if __name__ == '__main__':
    main()
