#!/usr/bin/env python3

from datetime import datetime

SWITCHES = [
    {
        "name": "User_Network",
        "ip": "10.10.1.24",
        "platform": "extreme_exos",
        "config_data": {
            "vlan_purpose": "User Network access layer VLAN",
            "connected_to": "Local_Switch (10.10.1.20)",
            "ssh_enabled": True,
        },
    },
    {
        "name": "ACCT_Network",
        "ip": "10.10.1.23",
        "platform": "extreme_exos",
        "config_data": {
            "vlan_purpose": "Accounting Network access layer VLAN",
            "connected_to": "Local_Switch (10.10.1.20)",
            "ssh_enabled": True,
        },
    },
    {
        "name": "MGMT_Network",
        "ip": "10.10.1.22",
        "platform": "extreme_exos",
        "config_data": {
            "vlan_purpose": "Management Network access layer VLAN",
            "connected_to": "Local_Switch (10.10.1.20)",
            "ssh_enabled": True,
        },
    },
    {
        "name": "IT_Network",
        "ip": "10.10.1.21",
        "platform": "extreme_exos",
        "config_data": {
            "vlan_purpose": "IT Network access layer VLAN",
            "connected_to": "Local_Switch (10.10.1.20)",
            "ssh_enabled": True,
        },
    },
]

OUTPUT_FILE = "switch_inventory.ini"


def print_switch_details():
    print(f"Script run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for switch in SWITCHES:
        print(f"Switch Name: {switch['name']}")
        print(f"Switch IP Address: {switch['ip']}")
        print(f"Platform: {switch['platform']}")

        for key, value in switch["config_data"].items():
            print(f"{key}: {value}")

        print()


def write_inventory_file():
    with open(OUTPUT_FILE, "w") as f:
        f.write("[switches]\n")

        for switch in SWITCHES:
            f.write(
                f"{switch['name']} "
                f"ansible_host={switch['ip']} "
                f"platform={switch['platform']}\n"
            )

        f.write("\n[switches:vars]\n")
        f.write("ansible_connection=network_cli\n")
        f.write("ansible_network_os=extreme.exos.exos\n")

        for switch in SWITCHES:
            f.write(f"\n# {switch['name']} configuration data\n")

            for key, value in switch["config_data"].items():
                f.write(
                    f"# {switch['name']}_{key} = {value}\n"
                )

    print(f"Inventory file written to: {OUTPUT_FILE}")


def main():
    print_switch_details()
    write_inventory_file()


if __name__ == "__main__":
    main()
