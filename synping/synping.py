#!/usr/bin/python

# synping 0.7
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 05/02/2017

import socket
import time
import sys
import optparse


version = '0.7'


# Parse and validate arguments
def get_parsed_args():
    usage = 'usage: %prog host [options]'
    # Create the parser
    parser = optparse.OptionParser(
        description='ping hosts using tcp syn packets',
        usage=usage, version=version
    )
    parser.add_option('-t', action='store_true', default=False,
                      help="ping host until stopped with 'control-c'")
    parser.add_option('-n', dest='count', default=4, type=int,
                      help="number of requests to send (default: %default)")
    parser.add_option('-p', dest='port', default=80, type=int,
                      help="port number to use (default: %default)")
    parser.add_option('-w', dest='timeout', default=3, type=int,
                      help="timeout in seconds to wait for reply \
                        (default: %default)")

    # Print help if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Parse the args
    (options, args) = parser.parse_args()

    # Some args validation
    if len(args) == 0:
        parser.error('host not informed')
    if len(args) > 1:
        parser.error('incorrect number of arguments')
    if options.port <= 0 or options.port > 65535:
        parser.error('port must be a number between 1 and 65535')
    if options.timeout < 1:
        parser.error('timeout must be a positive number')
    if options.count <= 0:
        parser.error('count must be a positive number')
    return (options, args)


# Get the host IP
def get_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except Exception, ex:
        if 'Errno' in str(ex) or '-2' in str(ex) or 'not know' in str(ex):
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


# Main CLI
def cli():
    (options, args) = get_parsed_args()
    host = args[0]

    # Needed variables
    times = []
    rcvd = 0
    sent = 0
    total = 0

    # Get the host IP
    remote_ip = get_ip(host)

    # Print the appropriate beginning message
    if not options.t:
        print '\nPinging %s %d times on port %d:\n'\
            % (host, options.count, options.port)
    else:
        print '\nPinging %s on port %d:\n' % (host, options.port)

    # Begin the pinging
    try:
        while True:
            # Timer needed for refused connections
            tr0 = time.time()
            try:
                tt = ping(remote_ip, options.port, options.timeout)
                times.append(tt)
                sent += 1
                rcvd += 1
                print 'Reply from %s:%d time=%.2f ms'\
                    % (remote_ip, options.port, tt * 1000)
            except Exception, ex:
                tr1 = time.time()
                # If the host respond with a refused message it means it is
                # alive, 111 and 10061 are Errno codes for linux and windows
                if '111' in str(ex) or '10061' in str(ex)\
                        or 'refused' in str(ex):
                    ttr = tr1 - tr0
                    times.append(ttr)
                    sent += 1
                    rcvd += 1
                    print 'Reply from %s:%d time=%.2f ms'\
                        % (remote_ip, options.port, ttr * 1000)
                elif 'timed out' in str(ex):
                    sent += 1
                    print (
                        'Timed out after ' + str(options.timeout) +
                        ' seconds'
                    )
                elif '22' in str(ex) or 'argument' in str(ex):
                    print 'error: invalid host'
                    sys.exit(1)
                else:
                    sent += 1
                    print ex
            # End the loop if needed
            if not options.t:
                if sent == options.count:
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
    print '\nHost: %s\n' % host
    print (
        "Sent: %d packets\nReceived: %d packets\n"
        "Lost: %d packets (%.2f%%)\n"
    ) % (sent, rcvd, sent - rcvd, float(sent - rcvd) / sent * 100)
    print 'Min time: %.2f ms\nMax time: %.2f ms\nAverage time: %.2f ms'\
        % (min(times) * 1000, max(times) * 1000, average * 1000)


# Run main function if invoked from shell
if __name__ == '__main__':
    cli()
