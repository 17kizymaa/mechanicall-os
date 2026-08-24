#!/usr/bin/env python3
"""TCP hop: 127.0.0.1:11434 -> myarch Ollama. Run on mbp-edge. Not Decide."""
from __future__ import annotations

import socket
import sys
import threading

LISTEN = ("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 11434)
DEST = (sys.argv[2] if len(sys.argv) > 2 else "100.90.85.68", 11434)


def pipe(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    try:
        src.close()
        dst.close()
    except OSError:
        pass


def main() -> None:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(LISTEN)
    server.listen(16)
    while True:
        client, _ = server.accept()
        try:
            upstream = socket.create_connection(DEST, timeout=4)
        except OSError:
            client.close()
            continue
        threading.Thread(target=pipe, args=(client, upstream), daemon=True).start()
        threading.Thread(target=pipe, args=(upstream, client), daemon=True).start()


if __name__ == "__main__":
    main()
