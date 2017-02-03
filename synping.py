#!/usr/bin/python

# synping 0.2
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 03/02/2017

import socket
import time
import sys
import argparse


# Parse and validate arguments
def get_parsed_args():
    # Create the parser
    parser = argparse.ArgumentParser(
        description='ping hosts using tcp syn packets', version='0.2')
    parser.add_argument('host', type=str, help='hostname or IP to ping')
    parser.add_argument('-t', action='store_true', default=False,
                        help="ping host until stopped with 'control-c'")
    parser.add_argument('-n', dest='count', metavar='COUNT', default=4,
                        type=int, help="number of requests to send")
    parser.add_argument('-p', dest='port', default=80, type=int,
                        help="port number to use (default: 80)")
    parser.add_argument('-w', dest='timeout', default=3, type=int,
                        help="timeout in seconds to wait for reply \
                        (default: 3)")

    # Print help if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Parse the args
    args = parser.parse_args()

    # Some args validation
    if args.port <= 0 or args.port > 65535:
        print '\nerror: port must be a number between 1 and 65535'
        sys.exit(2)
    if args.timeout < 1:
        print '\nerror: timeout must be a positive number'
        sys.exit(2)
    if args.count <= 0:
        print '\nerror: count must be a positive number'
        sys.exit(2)
    return args


# Get the host IP
def get_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except Exception as ex:
        if 'not know' in str(ex):
            print '\nerror: unknown host'
        else:
            print ex
        sys.exit(1)
    return remote_ip


# Ping the host
def ping(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    t0 = time.time()
    s.connect((host, port))
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    t1 = time.time()
    tt = t1 - t0
    return tt


# Main
def main():
    args = get_parsed_args()

    # Needed variables
    times = []
    rcvd = 0
    sent = 0
    total = 0

    # Get the host IP
    remote_ip = get_ip(args.host)

    # Print the appropriate beginning message
    if not args.t:
        print '\nPinging %s %d times on port %d:\n'\
            % (args.host, args.count, args.port)
    else:
        print '\nPinging %s on port %d:\n' % (args.host, args.port)

    # Begin the pinging
    try:
        while True:
            # Timer needed for refused connections
            tr0 = time.time()
            try:
                tt = ping(remote_ip, args.port, args.timeout)
                times.append(tt)
                sent += 1
                rcvd += 1
                print 'Reply from %s:%d time=%.2f ms'\
                    % (remote_ip, args.port, tt * 1000)
            except Exception as ex:
                tr1 = time.time()
                # If the host respond with a refused message it means it is
                # alive
                if 'refused' in str(ex):
                    ttr = tr1 - tr0
                    times.append(ttr)
                    sent += 1
                    rcvd += 1
                    print 'Reply from %s:%d time=%.2f ms'\
                        % (remote_ip, args.port, ttr * 1000)
                elif 'timed out' in str(ex):
                    sent += 1
                    print 'Timed out after ' + str(args.timeout) + ' seconds'
                elif 'argument' in str(ex):
                    print 'error: invalid host\n'
                    sys.exit(1)
                else:
                    sent += 1
                    print ex
            # End the loop if needed
            if not args.t:
                if sent == args.count:
                    break
            # Sleep between the requests
            time.sleep(1)
    # Catch the keyboard interrupt to end the loop
    except KeyboardInterrupt:
        print '\nAborted.'

    # Early exit without sending packets
    if sent == 0:
        sys.exit(1)

    # If no packets received print appropriate message and end the program
    if rcvd == 0:
        print "\nDidn't receive any packets..."
        print "Host is probably DOWN or firewalled. Sorry :'("
        sys.exit(1)

    # Calculate the average time
    for t in times:
        total += t
    average = total / rcvd

    # Print the summary
    print '\nStatistics:'
    print '-' * 26
    print '\nHost: %s\n' % args.host
    print (
        "Sent: %d packets\nReceived: %d packets\n"
        "Lost: %d packets (%.2f%%)\n"
    ) % (sent, rcvd, sent - rcvd, float(sent - rcvd) / sent * 100)
    print 'Min time: %.2f ms\nMax time: %.2f ms\nAverage time: %.2f ms'\
        % (min(times) * 1000, max(times) * 1000, average * 1000)


# Run main function if invoked from shell
if __name__ == '__main__':
    main()
