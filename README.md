# Network Automation & Cloud Provisioning (Python · Ansible · Terraform)

Automating a multi-VLAN campus switch network with **Python/Netmiko** and **Ansible**, then provisioning and configuring a mixed Ubuntu/RHEL server fleet on **AWS** with **Terraform** and **Ansible**.

> Built for **WGU D417 – Network Automation and Deployment** (B.S. Cloud & Network Engineering). The scenario: a network engineer at an IT vendor that supports school districts replaces manual, box-by-box configuration with repeatable automation.

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Netmiko](https://img.shields.io/badge/Netmiko-SSH-informational)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)
![Extreme EXOS](https://img.shields.io/badge/Extreme-EXOS-6A1B9A)

---

## Project scope

### Problem
Configuring VLANs and local admin accounts one device at a time is slow, error-prone and hard to audit. The same goes for standing up servers by hand in the cloud.

### Objectives
| # | Objective | Delivered by |
|---|-----------|--------------|
| 1 | Inventory every access switch and generate an Ansible inventory | `get_switch_config.py` |
| 2 | Audit the VLANs on all switches | `check_vlans.py` |
| 3 | Create a department VLAN on each switch (IT 10, ACCT 20, MGMT 30, User 40) | `create_vlans.py` |
| 4 | Create a read/write `Local-Admin` account on every switch | `create_users.yml` |
| 5 | Provision one Ubuntu and one RHEL server on AWS from code | Terraform (`task2-cloud-provisioning/terraform`) |
| 6 | Create a privileged `AdminWGU` account on both OS families from one playbook | `create_admin_user.yml` |

### In scope
- SSH key-based automation against four Extreme Networks EXOS switches
- Idempotent account creation with Ansible (`extreme.exos` collection and the `user` module)
- Infrastructure as Code for EC2, a security group and a generated key pair
- OS-aware configuration: `sudo` on Debian/Ubuntu, `wheel` on RHEL

### Out of scope
- Inter-VLAN routing and trunk design (handled by the lab's core/local switch)
- Remote Terraform state, CI/CD pipelines, secrets management beyond runtime prompts

---

## Task 1 – Campus switch automation

### Topology

```mermaid
flowchart TB
    host["Automation host<br/>Python 3 + Netmiko + Ansible"]
    core["Local_Switch<br/>10.10.1.20"]
    host -- "SSH (key auth)" --> core

    subgraph closet["Access Closet 1 – Extreme EXOS switches"]
        it["IT_Network<br/>10.10.1.21<br/>VLAN 10"]
        acct["ACCT_Network<br/>10.10.1.23<br/>VLAN 20"]
        mgmt["MGMT_Network<br/>10.10.1.22<br/>VLAN 30"]
        user["User_Network<br/>10.10.1.24<br/>VLAN 40"]
    end

    core --- it
    core --- acct
    core --- mgmt
    core --- user
```

### Automation workflow

```mermaid
sequenceDiagram
    autonumber
    participant Eng as Engineer
    participant Py as Python / Netmiko
    participant Ans as Ansible
    participant SW as EXOS switches (x4)

    Eng->>Py: get_switch_config.py
    Py-->>Eng: switch details + switch_inventory.ini
    Eng->>Py: check_vlans.py
    Py->>SW: show vlan
    SW-->>Py: existing VLANs (baseline)
    Eng->>Py: create_vlans.py
    Py->>SW: create vlan <name> / configure vlan <name> tag <id>
    SW-->>Py: show vlan (confirms new VLAN)
    Eng->>Ans: ansible-playbook create_users.yml
    Ans->>SW: create account admin Local-Admin
    Ans->>SW: show account
    SW-->>Ans: Local-Admin present on all 4 switches
```

### VLAN plan

| Switch | Mgmt IP | VLAN name | VLAN ID |
|--------|---------|-----------|---------|
| IT_Network | 10.10.1.21 | IT_Network | 10 |
| ACCT_Network | 10.10.1.23 | ACCT_Network | 20 |
| MGMT_Network | 10.10.1.22 | MGMT_Network | 30 |
| User_Network | 10.10.1.24 | User_Network | 40 |

---

## Task 2 – Cloud server provisioning

### Architecture

```mermaid
flowchart LR
    subgraph local["Engineer workstation"]
        tf["Terraform"]
        ans["Ansible"]
    end

    subgraph aws["AWS us-west-2 – existing lab VPC"]
        kp["aws_key_pair<br/>(generated RSA 2048)"]
        sg["Security group<br/>d417-task2-sg<br/>SSH 22 in"]
        ub["EC2 t2.micro<br/>D417-Ubuntu-Server"]
        rh["EC2 t2.micro<br/>D417-RHEL-Server"]
        sg --- ub
        sg --- rh
        kp --- ub
        kp --- rh
    end

    tf -- "plan / apply" --> aws
    tf -. "writes .pem + outputs public IPs" .-> ans
    ans -- "SSH: create AdminWGU<br/>sudo / wheel" --> ub
    ans -- "SSH: create AdminWGU<br/>sudo / wheel" --> rh
```

### Pipeline

```mermaid
flowchart LR
    A["terraform init"] --> B["terraform apply"] --> C["terraform output<br/>public IPs"] --> D["fill inventory.ini"] --> E["ansible-playbook<br/>create_admin_user.yml"] --> F["id AdminWGU<br/>verification"]
```

Terraform resources: `tls_private_key`, `aws_key_pair`, `local_file` (private key, mode 0400), `aws_security_group`, two `aws_instance`, plus data sources that look up the existing lab VPC and subnets by tag.

---

## Repository structure

```
.
├── requirements.txt
├── task1-switch-automation/
│   ├── scripts/            # Netmiko scripts: inventory, VLAN audit, VLAN creation
│   ├── ansible/            # Inventories + Local-Admin playbook (EXOS)
│   └── outputs/            # Captured run output from the lab
└── task2-cloud-provisioning/
    ├── terraform/          # provider, key pair, security group, Ubuntu + RHEL EC2, outputs
    ├── ansible/            # Cross-distro admin-user playbook + example inventory
    └── outputs/            # terraform apply / ansible run output
```

## Running it

```bash
pip install -r requirements.txt
ansible-galaxy collection install extreme.exos
```

**Task 1** (needs SSH reachability to the switches):
```bash
cd task1-switch-automation/scripts
python3 get_switch_config.py
python3 check_vlans.py
python3 create_vlans.py
cd ../ansible
ansible-playbook -i inventory.ini create_users.yml   # prompts for the Local-Admin password
```

**Task 2** (needs AWS credentials in your environment):
```bash
cd task2-cloud-provisioning/terraform
terraform init && terraform apply
terraform output
cd ../ansible
cp inventory.example.ini inventory.ini     # paste the IPs from terraform output
ADMIN_PASSWORD='choose-one' ansible-playbook -i inventory.ini create_admin_user.yml
terraform -chdir=../terraform destroy      # clean up when done
```

## Results

- 4/4 switches inventoried and audited, with the correct VLAN created and tagged on each one ([outputs](task1-switch-automation/outputs))
- `Local-Admin` created and verified on all switches with one playbook run
- Ubuntu and RHEL servers built from code in a single `terraform apply`
- One playbook handled both OS families by choosing the admin group from `ansible_facts['os_family']` ([output](task2-cloud-provisioning/outputs/ansible_output.txt))

## What I'd improve next

- Move the switch list into a YAML or inventory file shared by the Python scripts and Ansible, so it lives in one place
- Make `create_vlans.py` idempotent (skip if the VLAN already exists) and add `--dry-run`
- Use Ansible Vault for credentials and restrict the security group's SSH rule to a known CIDR, not `0.0.0.0/0`
- Store Terraform state remotely (S3 + DynamoDB lock) and add `terraform fmt`/`validate`/`tflint` in CI

---

<sub>Academic project completed at Western Governors University. Lab IPs are from a disposable training environment, and passwords have been removed from the code and captured output.</sub>
