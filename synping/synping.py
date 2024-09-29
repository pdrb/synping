#!/usr/bin/env python3

# synping 1.0
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 20240929

import argparse
import socket
import sys
import time

_version = "1.0"


def parse_args() -> argparse.Namespace:
    """Parse and validate arguments."""
    # Create parser
    parser = argparse.ArgumentParser(
        prog="synping",
        usage="%(prog)s host [options]",
        description="ping hosts using tcp syn packets",
        epilog="e.g.: %(prog)s example.org",
    )

    # Arguments
    parser.add_argument(
        "host",
        help="host to ping",
    )
    parser.add_argument(
        "-t",
        action="store_true",
        default=False,
        help="ping host until stopped with 'control-c'",
    )
    parser.add_argument(
        "-n",
        dest="count",
        default=4,
        type=int,
        help="number of requests to send (default: %(default)s)",
    )
    parser.add_argument(
        "-p",
        dest="port",
        default=80,
        type=int,
        help="port to ping (default: %(default)s)",
    )
    parser.add_argument(
        "-w",
        dest="timeout",
        default=3,
        type=float,
        help="timeout in seconds to wait for reply (default: %(default)s)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=_version,
    )

    # Print help if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Parse arguments
    args = parser.parse_args()

    # Validate arguments
    if args.port <= 0 or args.port > 65535:
        parser.error("port must be a number between 1 and 65535")
    if args.timeout <= 0:
        parser.error("timeout must be greater than 0")
    if args.count <= 0:
        parser.error("count must be a positive number")

    return args


def get_ip(host: str) -> str:
    """Get the host IP."""
    try:
        remote_ip = socket.gethostbyname(host)
    except Exception as ex:
        print(f"Error: {repr(ex)}")
        sys.exit(1)
    return remote_ip


def ping(host: str, port: int, timeout: float) -> float:
    """Ping host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    init_time = time.time()
    try:
        s.connect((host, port))
    except Exception as ex:
        # Catches "[Errno 22] Invalid argument" on Linux, e.g., synping 1
        if "22" in str(ex) or "argument" in str(ex):
            print(f"error: invalid host: {host}")
            sys.exit(1)
        # Refused in error means host is alive
        if "refused" not in str(ex):
            raise ex
    end_time = time.time()
    s.close()
    return (end_time - init_time) * 1000


def cli():
    """Main CLI."""
    args = parse_args()

    # Variables
    rcvd = 0
    sent = 0
    total_time = 0

    # Get the host IP
    remote_ip = get_ip(args.host)

    # Print appropriate beginning message
    if not args.t:
        print(f"\nPinging {args.host} {args.count} times on port {args.port}:\n")
    else:
        print(f"\nPinging {args.host} on port {args.port}:\n")

    # Begin the pinging
    try:
        while True:
            try:
                ping_time = ping(remote_ip, args.port, args.timeout)
                sent += 1
                rcvd += 1
                # Initialize min and max time
                if rcvd == 1:
                    min_time = ping_time
                    max_time = ping_time
                # Update min and max if needed
                if ping_time < min_time:
                    min_time = ping_time
                if ping_time > max_time:
                    max_time = ping_time
                # Update the total time for calculating avg later
                total_time += ping_time
                print(f"Reply from {remote_ip}:{args.port} time={ping_time:.2f} ms")
            except Exception as ex:
                if "timed out" in str(ex):
                    sent += 1
                    print(f"Timed out after {args.timeout} seconds")
                else:
                    sent += 1
                    print(ex)
            # End the loop if needed
            if not args.t:
                if sent == args.count:
                    break
            # Sleep between the requests
            time.sleep(1)
    # Catch keyboard interrupt to end the loop
    except KeyboardInterrupt:
        print("\nAborted.")

    # Early exit without sending packets
    if sent == 0:
        sys.exit(1)

    # If no packets received print appropriate message and end the program
    if rcvd == 0:
        print("\nDidn't receive any packets...")
        print("Host is probably DOWN or firewalled. Sorry :'(\n")
        sys.exit(1)

    # Print the summary
    print("\nStatistics:")
    print("-" * 26)
    print(f"\nHost: {args.host}\n")
    print(f"Sent: {sent} packets")
    print(f"Received: {rcvd} packets")
    print(f"Lost: {sent - rcvd} packets ({float(sent - rcvd) / sent * 100:.2f})%\n")
    print(f"Min time: {min_time:.2f} ms")
    print(f"Max time: {max_time:.2f} ms")
    print(f"Average time: {total_time / rcvd:.2f} ms\n")


# Run main function if invoked from shell
if __name__ == "__main__":
    cli()
