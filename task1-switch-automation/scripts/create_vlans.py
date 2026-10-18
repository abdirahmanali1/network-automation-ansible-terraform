#!/usr/bin/env python3

from netmiko import ConnectHandler

USERNAME = "student"

SWITCHES = [
    {
        "name": "IT_Network",
        "ip": "10.10.1.21",
        "key_file": "~/.ssh/id_rsa",
        "vlan_name": "IT_Network",
        "vlan_id": 10,
    },
    {
        "name": "MGMT_Network",
        "ip": "10.10.1.22",
        "key_file": "~/.ssh/id_rsa",
        "vlan_name": "MGMT_Network",
        "vlan_id": 30,
    },
    {
        "name": "ACCT_Network",
        "ip": "10.10.1.23",
        "key_file": "~/.ssh/id_rsa",
        "vlan_name": "ACCT_Network",
        "vlan_id": 20,
    },
    {
        "name": "User_Network",
        "ip": "10.10.1.24",
        "key_file": "~/.ssh/id_rsa",
        "vlan_name": "User_Network",
        "vlan_id": 40,
    },
]


def create_vlan(switch_name, switch_ip, key_file, vlan_name, vlan_id):
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

        commands = [
            f"create vlan {vlan_name}",
            f"configure vlan {vlan_name} tag {vlan_id}",
        ]

        print(f"Connecting to {switch_name} ({switch_ip})...")
        print(f"Creating VLAN {vlan_name} with tag {vlan_id}...")

        for cmd in commands:
            output = conn.send_command(cmd, expect_string=r"#")
            print(f"$ {cmd}")

            if output.strip():
                print(output)

        output = conn.send_command("show vlan")
        print(output)

        conn.disconnect()

        print(f"SUCCESS: VLAN {vlan_name} created on {switch_name}.")
        return True

    except Exception as e:
        print(f"ERROR: {switch_name} ({switch_ip}): {e}")
        return False


def main():
    success_count = 0

    for switch in SWITCHES:
        if create_vlan(
            switch["name"],
            switch["ip"],
            switch["key_file"],
            switch["vlan_name"],
            switch["vlan_id"],
        ):
            success_count += 1

    print(f"{success_count}/{len(SWITCHES)} VLANs created successfully.")


if __name__ == "__main__":
    main()
