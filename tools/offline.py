#!/usr/bin/env python3
"""Run a Python script with network access disabled.

Usage: python3 tools/offline.py <script.py> [args...]

Patches socket connect, create_connection and getaddrinfo to raise OSError
before the script runs, so an example that tries the network fails instead of
quietly passing. tools/validate.py runs every examples/minimal.py through this,
and calls block_network() on itself.
"""
import os
import runpy
import socket
import sys


def _refuse(*_a, **_k):
    raise OSError("network access disabled by tools/offline.py")


def block_network():
    socket.socket.connect = _refuse
    socket.socket.connect_ex = _refuse
    socket.create_connection = _refuse
    socket.getaddrinfo = _refuse


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: offline.py <script.py> [args...]")
    block_network()
    sys.argv = sys.argv[1:]
    sys.path[0] = os.path.dirname(os.path.abspath(sys.argv[0]))
    runpy.run_path(sys.argv[0], run_name="__main__")
