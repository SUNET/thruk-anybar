#!/usr/bin/env python3

import os.path
import socket
import subprocess
import sys
import time
import traceback
from json import JSONDecodeError

import psutil
import requests
import toml


def write_to_socket(*, host="127.0.0.1", color, site, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(bytes(f"{site}-{color}", "utf-8"), (host, port))


def anybar_ports():
    """Return the UDP ports that running AnyBar instances listen on."""
    ports = []
    for proc in psutil.process_iter():
        try:
            if proc.name() == "AnyBar":
                for conn in proc.net_connections(kind="udp"):
                    laddr = getattr(conn, "laddr")
                    lport = getattr(laddr, "port")
                    ports.append(lport)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return ports


def wait_for_port(port, timeout=10):
    """Poll until an AnyBar instance listens on port; return whether it does."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if port in anybar_ports():
            return True
        time.sleep(0.2)
    return False


def check_site(site, site_config, opened_anybar_ports):
    status_color = "red"
    baseurl = site_config["baseurl"]
    key = site_config["key"]
    port = site_config["port"]
    thrukurl = f"{baseurl}/thruk/r/services"

    if port not in opened_anybar_ports:
        env = {
            "ANYBAR_TITLE": site,
            "ANYBAR_PORT": str(port),
            "ANYBAR_INIT": f"{site}-black",
        }
        subprocess.Popen(["open", "-g", "-n", "-a", "AnyBar"], env=env)
        if not wait_for_port(port):
            print(f"{site}: AnyBar did not open port {port}", file=sys.stderr)

    if os.path.exists("/tmp/awol"):
        status_color = "yellow"
        write_to_socket(color=status_color, site=site, port=port)
        return

    # XXX - configureable params per site?
    params = {
        "acknowledged": 0,
        "state[ne]": 0,
        "scheduled_downtime_depth": 0,
    }
    headers = {
        "X-Thruk-Auth-Key": key,
    }

    try:
        r = requests.get(thrukurl, params=params, headers=headers, timeout=(5, 30))
    except requests.exceptions.RequestException:
        status_color = "black"
        write_to_socket(color=status_color, site=site, port=port)
        return

    try:
        r.raise_for_status()
        data = r.json()
    except (requests.exceptions.HTTPError, JSONDecodeError):
        status_color = "purple"
        write_to_socket(color=status_color, site=site, port=port)
        return

    if len(data) == 0:
        status_color = "green"

    write_to_socket(color=status_color, site=site, port=port)


def main():
    config_path = f"{os.path.expanduser('~')}/.Anybar/thruk-anybar.toml"
    try:
        with open(config_path, "r") as f:
            config = toml.load(f)
    except (OSError, toml.TomlDecodeError) as e:
        sys.exit(f"Cannot read {config_path}: {e}")

    opened_anybar_ports = anybar_ports()

    for site, site_config in config.items():
        try:
            check_site(site, site_config, opened_anybar_ports)
        except Exception:
            print(f"{site}: unexpected error", file=sys.stderr)
            traceback.print_exc()
            try:
                write_to_socket(color="black", site=site, port=site_config["port"])
            except Exception:
                pass


if __name__ == "__main__":
    main()
