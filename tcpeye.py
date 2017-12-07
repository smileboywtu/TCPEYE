# -*- coding: utf-8 -*-

"""

MIT License

Copyright (c) 2017 Bob

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import signal
import socket
import sys
import time
from argparse import ArgumentParser

ERRORS = [
    'Success',
    'Operation not permitted',
    'No such file or directory',
    'No such process',
    'Interrupted system call',
    'Input/output error',
    'No such device or address',
    'Argument list too long',
    'Exec format error',
    'Bad file descriptor',
    'No child processes',
    'Resource temporarily unavailable',
    'Cannot allocate memory',
    'Permission denied',
    'Bad address',
    'Block device required',
    'Device or resource busy',
    'File exists',
    'Invalid cross-device link',
    'No such device',
    'Not a directory',
    'Is a directory',
    'Invalid argument',
    'Too many open files in system',
    'Too many open files',
    'Inappropriate ioctl for device',
    'Text file busy',
    'File too large',
    'No space left on device',
    'Illegal seek',
    'Read-only file system',
    'Too many links',
    'Broken pipe',
    'Numerical argument out of domain',
    'Numerical result out of range',
    'Resource deadlock avoided',
    'File name too long',
    'No locks available',
    'Function not implemented',
    'Directory not empty',
    'Too many levels of symbolic links',
    'Unknown error 41',
    'No message of desired type',
    'Identifier removed',
    'Channel number out of range',
    'Level 2 not synchronized',
    'Level 3 halted',
    'Level 3 reset',
    'Link number out of range',
    'Protocol driver not attached',
    'No CSI structure available',
    'Level 2 halted',
    'Invalid exchange',
    'Invalid request descriptor',
    'Exchange full',
    'No anode',
    'Invalid request code',
    'Invalid slot',
    'Unknown error 58',
    'Bad font file format',
    'Device not a stream',
    'No data available',
    'Timer expired',
    'Out of streams resources',
    'Machine is not on the network',
    'Package not installed',
    'Object is remote',
    'Link has been severed',
    'Advertise error',
    'Srmount error',
    'Communication error on send',
    'Protocol error',
    'Multihop attempted',
    'RFS specific error',
    'Bad message',
    'Value too large for defined data type',
    'Name not unique on network',
    'File descriptor in bad state',
    'Remote address changed',
    'Can not access a needed shared library',
    'Accessing a corrupted shared library',
    '.lib section in a.out corrupted',
    'Attempting to link in too many shared libraries',
    'Cannot exec a shared library directly',
    'Invalid or incomplete multibyte or wide character',
    'Interrupted system call should be restarted',
    'Streams pipe error',
    'Too many users',
    'Socket operation on non-socket',
    'Destination address required',
    'Message too long',
    'Protocol wrong type for socket',
    'Protocol not available',
    'Protocol not supported',
    'Socket type not supported',
    'Operation not supported',
    'Protocol family not supported',
    'Address family not supported by protocol',
    'Address already in use',
    'Cannot assign requested address',
    'Network is down',
    'Network is unreachable',
    'Network dropped connection on reset',
    'Software caused connection abort',
    'Connection reset by peer',
    'No buffer space available',
    'Transport endpoint is already connected',
    'Transport endpoint is not connected',
    'Cannot send after transport endpoint shutdown',
    'Too many references: cannot splice',
    'Connection timed out',
    'Connection refused',
    'Host is down',
    'No route to host',
    'Operation already in progress',
    'Operation now in progress',
    'Stale NFS file handle',
    'Structure needs cleaning',
    'Not a XENIX named type file',
    'No XENIX semaphores available',
    'Is a named type file',
    'Remote I/O error',
    'Disk quota exceeded',
    'No medium found',
    'Wrong medium type'
]

STDOUT = "{ts} | " \
         "{host}:{ip}:{port} | " \
         "{tcpcode} | " \
         "{errmsg}"


def args_parser():
    parser = ArgumentParser(description="TCP EYE DAEMON")
    parser.add_argument(
        "-d", "--period",
        type=int,
        default=1,
        dest="PERIOD",
        metavar="VALUE",
        help="TCP check period time delta"
    )
    parser.add_argument(
        "-H", "--host",
        type=str,
        default="127.0.0.1",
        dest="HOST",
        metavar="VALUE",
        help="Host to check"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=22,
        dest="PORT",
        metavar="VALUE",
        help="Port to check"
    )
    return parser.parse_args()


def eye(host, port):
    """
    eye on TCP connection

    :param host:
    :param port:
    :return:
    """
    try:
        ts = int(time.time())
        ip = socket.gethostbyname(host)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        errcode = sock.connect_ex((host, port))
    except socket.error:
        if socket.errno <= len(ERRORS):
            errcode = socket.errno
            errmsg = ERRORS[socket.errno]
    except socket.timeout:
        errcode = -1
        errmsg = "connect timeout"
    except Exception as e:
        errcode = -2
        errmsg = str(e)
    finally:
        print STDOUT.format(
            ts=ts,
            host=host,
            ip=ip,
            port=port,
            tcpcode=errcode,
            errmsg=errmsg
        )
        sock.close()


def exit_handler(signal, frame):
    sys.exit(0)


if __name__ == "__main__":
    args = args_parser()

    signal.signal(signal.SIGINT, exit_handler)

    while True:
        eye(args.HOST, args.PORT)
        time.sleep(args.PERIOD)
