import argparse
import json
import subprocess

import requests


def get_ip_info(ip: str):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response_json = json.loads(response.content)
        return response_json['hostname'], \
               response_json['org'], \
               response_json["country"]

    except Exception:
        return None


def tracer(destination):
    p = subprocess.Popen([f'traceroute', destination], stdout=subprocess.PIPE)

    out = p.communicate()[0].decode()

    for i in enumerate(out.split('\n')[1:-1], start=1):
        ip = i[1].split()[2]
        if ip == '*':
            continue

        ip = ip[1:-1]
        info = get_ip_info(ip)

        print(f'{i[0]}\t{ip}')

        if info is None:
            print()
            continue

        print(f'\thostname: {info[0]}')
        print(f'\torg: {info[1]}')
        print(f'\tcountry: {info[2]}')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=str)

    args = parser.parse_args()

    tracer(args.destination)
