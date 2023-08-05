import os
import argparse
import paramiko
from fuzzywuzzy import process

def connect(host: str):
    os.system(f'ssh {host}')

def connect_to_user_selected(hosts: list[str]):
    # Let user select
    ss = '#\tHost\n'
    for idx in range(len(hosts)):
        host = hosts[idx]
        ss += f'{idx}\t{host}\n'
    ss += 'Select Index or Host: [0]'
    print(ss, end=" ", flush=True)

    try:
        selected = input()
    except KeyboardInterrupt:
        print('\nUser cancelled')
        return
    # default to 0
    if not selected:
        selected = '0'
    # user input host
    if not selected.isdigit():
        connect(selected)
        return

    # user input index
    try:
        selected_idx = int(selected)
    except ValueError:
        print('Invalid input')
        return
    if selected_idx >= len(hosts):
        print(f'Index must be less than {len(hosts)}')
        return
    # Connect
    host = hosts[selected_idx]
    connect(host)

def parse_sys_args():
    parser = argparse.ArgumentParser(
                        prog='kkssh',
                        description='ssh wrapper')

    parser.add_argument('-c', '--config', required=False, default='~/.ssh/config')
    parser.add_argument('--editor', default='code')
    parser.add_argument('-e', '--edit', action='store_true')
    parser.add_argument('hostname', nargs='?')
    return parser.parse_args()

def main():
    # Parse arguments
    args = parse_sys_args()
    ssh_config_path = args.config
    target_host = args.hostname

    if args.edit:
        print(f'Opening {ssh_config_path}')
        os.system(f'{args.editor} {ssh_config_path}')
        return

    # Load ssh config
    ssh_config = paramiko.SSHConfig()
    with open(ssh_config_path) as f:
        ssh_config.parse(f)
    hosts = sorted([i for i in ssh_config.get_hostnames() if i != '*' ])

    # No hostname provided, let user select
    if not target_host:
        connect_to_user_selected(hosts)
        return

    # Direct connect if hostname match
    if target_host in hosts:
        connect(target_host)
        return

    # Fuzzy search
    matches = process.extract(target_host, hosts)
    if not matches:
        print('Not found')
        return
    match_hosts = [i[0] for i in matches]
    connect_to_user_selected(match_hosts)

if __name__ == '__main__':
    main()
