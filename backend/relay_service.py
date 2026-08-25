import socket

RELAY_HOST = "127.0.0.1"
RELAY_PORT = 1025


def is_relay_running() -> bool:
    try:
        with socket.create_connection((RELAY_HOST, RELAY_PORT), timeout=1):
            return True
    except OSError:
        return False


def get_relay_status() -> dict:
    running = is_relay_running()
    return {
        "running": running,
        "host": RELAY_HOST,
        "port": RELAY_PORT,
        "status": "online" if running else "offline",
    }
