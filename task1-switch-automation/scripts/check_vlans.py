#!/usr/bin/env python3

from netmiko import ConnectHandler

USERNAME = "student"

SWITCHES = [
    {"name": "IT_Network", "ip": "10.10.1.21", "key_file": "~/.ssh/id_rsa"},
    {"name": "MGMT_Network", "ip": "10.10.1.22", "key_file": "~/.ssh/id_rsa"},
    {"name": "ACCT_Network", "ip": "10.10.1.23", "key_file": "~/.ssh/id_rsa"},
    {"name": "User_Network", "ip": "10.10.1.24", "key_file": "~/.ssh/id_rsa"},
]


def check_vlans(switch_name, switch_ip, key_file):
    device = {
        "device_type": "extreme_exos",
        "host": switch_ip,
        "username": USERNAME,
        "use_keys": True,
        "key_file": key_file,
        "disabled_algorithms": {"pubkeys": []},
    }

    try:
        conn = ConnectHandler(**device)
        output = conn.send_command("show vlan")

        print(f"Switch Name: {switch_name}")
        print(f"Switch IP: {switch_ip}")
        print("Existing VLANs:")
        print(output)
        print()

        conn.disconnect()
        return True

    except Exception as e:
        print(f"ERROR: Could not connect to {switch_name} ({switch_ip}): {e}")
        return False


def main():
    success_count = 0

    for switch in SWITCHES:
        if check_vlans(
            switch["name"],
            switch["ip"],
            switch["key_file"]
        ):
            success_count += 1

    print(f"{success_count}/{len(SWITCHES)} switches checked successfully.")


if __name__ == "__main__":
    main()
