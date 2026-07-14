import sys
import os
import json
from datetime import datetime, timezone, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEBUCK_START_TIME') or os.getenv('KODEARENA_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEBUCK_USERNAME', os.getenv('KODEARENA_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER')))
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else (os.getenv('KODEBUCK_EXAM_CODE') or os.getenv('KODEARENA_EXAM_CODE') or 'UNKNOWN')

def verify_task():
    print("-" * 65)
    print(f"{'AZURE RESOURCE AUDIT (VM & NETWORKING)':^65}")
    print("-" * 65)

    total_score = 0
    results = {
        'tc1': False,
        'tc2': False,
        'tc3': False,
        'tc4': False,
        'tc5': False,
        'tc6': False
    }

    try:
        # Load Azure Credentials from the environment
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        tenant_id = os.environ.get("AZURE_TENANT_ID")
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")

        if not all([subscription_id, tenant_id, client_id, client_secret]):
            print("TC1: Resource Group Access [FAILED] (0/0)")
            print("     └─ [Reason]: Missing subscription_id, tenant_id, client_id, or client_secret.")
            return

        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        resource_client = ResourceManagementClient(credential, subscription_id)
        network_client = NetworkManagementClient(credential, subscription_id)
        compute_client = ComputeManagementClient(credential, subscription_id)

        # Resource configurations
        raw_username = USER_PREFIX
        if '@' in raw_username:
            raw_username = raw_username.split('@')[0]
        if '_' in raw_username:
            raw_username = raw_username.split('_')[0]
        username = raw_username.lower().replace('.', '-')
        rg_name = "rg-iRUN-LTM-Assessment"
        vnet_name = f"vnet-{username}"
        nsg_name = f"nsg-{username}"
        vm_name = f"vm-{username}"

        # TC1: Resource Group validation (0 Marks)
        tc1_passed = False
        try:
            resource_client.resource_groups.get(rg_name)
            tc1_passed = True
            print("TC1: Resource Group Access ............................ [PASSED] (0/0)")
        except Exception as e:
            print("TC1: Resource Group Access ............................ [FAILED] (0/0)")
            print(f"     └─ [Reason]: Pre-created Resource Group '{rg_name}' not found. Details: {e}")
            return

        results['tc1'] = tc1_passed

        # TC2: Virtual Network (VNet) + default Subnet config in eastasia (4 Marks)
        tc2_passed = False
        try:
            vnet = network_client.virtual_networks.get(rg_name, vnet_name)
            subnet = network_client.subnets.get(rg_name, vnet_name, "default")
            
            prefixes = vnet.address_space.address_prefixes if vnet.address_space else []
            subnet_prefix = subnet.address_prefix
            vnet_loc = vnet.location.lower().replace(" ", "")
            
            if vnet_loc != "eastasia":
                print("TC2: Virtual Network & Subnet Range ................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: VNet is in '{vnet.location}', expected 'eastasia'.")
            elif "10.0.0.0/16" in prefixes and subnet_prefix == "10.0.0.0/24":
                tc2_passed = True
                print("TC2: Virtual Network & Subnet Range ................... [PASSED] (4/4)")
            else:
                print("TC2: Virtual Network & Subnet Range ................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Address Space: {prefixes} (expected ['10.0.0.0/16']), Subnet range: {subnet_prefix} (expected '10.0.0.0/24').")
        except Exception as e:
            print("TC2: Virtual Network & Subnet Range ................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Virtual network '{vnet_name}' or subnet 'default' not found. Details: {str(e)}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 4

        # TC3: NSG existence and association (4 Marks)
        tc3_passed = False
        try:
            nsg = network_client.network_security_groups.get(rg_name, nsg_name)
            tc3_passed = True
            print("TC3: NSG Existence .................................... [PASSED] (4/4)")
        except Exception as e:
            print("TC3: NSG Existence .................................... [FAILED] (0/4)")
            print(f"     └─ [Reason]: Network Security Group '{nsg_name}' not found. Details: {str(e)}")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 4

        # TC4: NSG Inbound Firewall Rules (TCP SSH allowed on 22) (4 Marks)
        tc4_passed = False
        if results['tc3']:
            try:
                nsg = network_client.network_security_groups.get(rg_name, nsg_name)
                rules = nsg.security_rules if nsg.security_rules else []
                ssh_allowed = False
                for rule in rules:
                    if (rule.direction == "Inbound" and
                        rule.protocol in ["Tcp", "*"] and
                        rule.access == "Allow" and
                        (rule.destination_port_range == "22" or rule.destination_port_range == "*")):
                        ssh_allowed = True
                        break
                        
                if ssh_allowed:
                    tc4_passed = True
                    print("TC4: NSG Inbound SSH Port 22 Rule ..................... [PASSED] (4/4)")
                else:
                    print("TC4: NSG Inbound SSH Port 22 Rule ..................... [FAILED] (0/4)")
                    print("     └─ [Reason]: No inbound rule allowing TCP/SSH traffic on port 22 found.")
            except Exception as e:
                print("TC4: NSG Inbound SSH Port 22 Rule ..................... [FAILED] (0/4)")
                print(f"     └─ [Reason]: Error querying rules: {e}")
        else:
            print("TC4: NSG Inbound SSH Port 22 Rule ..................... [FAILED] (0/4)")
            print("     └─ [Reason]: NSG verification failed.")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 4

        # TC5: Ubuntu VM (Standard_B1s) running and linked (4 Marks)
        tc5_passed = False
        vm = None
        try:
            vm = compute_client.virtual_machines.get(rg_name, vm_name, expand='instanceView')
            
            vm_size = vm.hardware_profile.vm_size if vm.hardware_profile else ""
            os_publisher = vm.storage_profile.image_reference.publisher if vm.storage_profile and vm.storage_profile.image_reference else ""
            os_offer = vm.storage_profile.image_reference.offer if vm.storage_profile and vm.storage_profile.image_reference else ""
            vm_loc = vm.location.lower().replace(" ", "")
            
            statuses = [s.code for s in vm.instance_view.statuses] if vm.instance_view else []
            is_running = any("PowerState/running" in status for status in statuses)
            
            is_size_correct = vm_size.lower() in ["standard_b1s"]
            is_ubuntu = "canonical" in os_publisher.lower() and "ubuntu" in os_offer.lower()

            if vm_loc != "eastasia":
                print("TC5: VM Specifications & Running State ................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: VM is in '{vm.location}', expected 'eastasia'.")
            elif is_running and is_size_correct and is_ubuntu:
                tc5_passed = True
                print("TC5: VM Specifications & Running State ................ [PASSED] (4/4)")
            else:
                print("TC5: VM Specifications & Running State ................ [FAILED] (0/4)")
                print(f"     └─ [Reason]: Size={vm_size} (expected Standard_B1s), OS={os_publisher}/{os_offer} (expected Ubuntu), Running={is_running}")
        except Exception as e:
            print("TC5: VM Specifications & Running State ................ [FAILED] (0/4)")
            print(f"     └─ [Reason]: Virtual machine '{vm_name}' not found or instance view loading failed. Details: {str(e)}")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 4

        # TC6: VM Authentication Security (disable_password_authentication == True) (4 Marks)
        tc6_passed = False
        if vm:
            try:
                os_prof = vm.os_profile
                linux_conf = os_prof.linux_configuration if os_prof else None
                disable_pwd = linux_conf.disable_password_authentication if linux_conf else False
                
                if disable_pwd:
                    tc6_passed = True
                    print("TC6: SSH Key Authentication Enforced .................. [PASSED] (4/4)")
                else:
                    print("TC6: SSH Key Authentication Enforced .................. [FAILED] (0/4)")
                    print("     └─ [Reason]: Password authentication is not disabled.")
            except Exception as e:
                print("TC6: SSH Key Authentication Enforced .................. [FAILED] (0/4)")
                print(f"     └─ [Reason]: Error checking SSH configuration: {e}")
        else:
            print("TC6: SSH Key Authentication Enforced .................. [FAILED] (0/4)")
            print("     └─ [Reason]: Prerequisite VM not found.")

        results['tc6'] = tc6_passed
        if tc6_passed:
            total_score += 4

    except Exception as e:
        print(f"[FATAL ERROR] Audit script crashed: {e}")

    # Write test results for local agent evaluation parser
    print(f"\n[SCORE] {total_score}")

if __name__ == '__main__':
    verify_task()
