import argparse
import signal
import time
import socket
import sys

__author__ = "Andrew Tanner <andrew@refleqtive.com>"

class TimeoutException(Exception):
    """ Exception that gets thrown when the pattern search times out """
    pass

class ConnectException(Exception):
    """ Exception that gets thrown when a pattern match is found """
    pass

def service_waiter(host, port, timeout):
    def timeout_handler(signum, frame):
        raise TimeoutException()

    # set a signal handler for the alarm signal
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    while 1:
        time.sleep(1)
        srv_socket = socket.socket()
        srv_socket.settimeout(0.25)
        try:
            srv_socket.connect((host, port))
        except socket.error:
            # ignore connection failures, only concern is connecting or timeout
            continue

        raise ConnectException

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("host", type=str, default=False, help="ip address or host name")
    parser.add_argument("port", type=int, default=False, help="port of service to monitor")
    parser.add_argument("-t", "--timeout", type=int, default=60,
                        help="desired timeout (defaults to 60 sec)")

    wait_args = parser.parse_args()

    try:
        service_waiter(wait_args.host, wait_args.port, wait_args.timeout)
    except ConnectException, e:
        print "Success: Service on host %s port %d is up" % (wait_args.host, wait_args.port)
        sys.exit(0)
    except TimeoutException, e:
        print "Failure: Hit timeout waiting for service on host %s port %d to receive connection" % \
              (wait_args.host, wait_args.port)
        sys.exit(1)

