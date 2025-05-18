# STOLEN FROM CHATGPT
# GETS DOCKER COMPOSE TO WORK

import socket
import time
import sys

def wait_for(host: str, port: int, timeout: int = 30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"Connected to {host}:{port}")
                return
        except OSError:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                print(f"Timeout, could not connect to {host}:{port}")
                sys.exit(1)

if __name__ == "__main__":
    import os

    host = sys.argv[1] if len(sys.argv) > 1 else os.getenv("WAIT_HOST", "db")
    port = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.getenv("WAIT_PORT", 5432))

    print(f"Waiting for {host}:{port} to become available...")
    wait_for(host, port)