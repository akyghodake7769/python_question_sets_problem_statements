import sys
import os
import json
from datetime import datetime, timezone, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

# Capture Assessment Start Time
START_TIME_STR = os.getenv('KODEARENA_START_TIME')
START_TIME = datetime.fromisoformat(START_TIME_STR.strip().replace('Z', '+00:00')) if START_TIME_STR else None
USER_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.getenv('KODEARENA_USERNAME', os.getenv('LABSKRAFT_USERNAME', 'LOCAL_USER'))
EXAM_CODE = sys.argv[3] if len(sys.argv) > 3 else 'UNKNOWN'

def verify_task():
    print("-" * 65)
    print(f"{'AZURE RESOURCE AUDIT':^65}")
    print("-" * 65)

    total_score = 0
    results = {
        'tc1': False,
        'tc2': False,
        'tc3': False,
        'tc4': False,
        'tc5': False
    }

    try:
        # Load Azure Credentials from the environment
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        tenant_id = os.environ.get("AZURE_TENANT_ID")
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")

        if not all([subscription_id, tenant_id, client_id, client_secret]):
            print("TC1: Environment Verification ......................... [FAILED] (0/0)")
            print("     └─ [Reason]: Missing subscription_id, tenant_id, client_id, or client_secret.")
            return

        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        resource_client = ResourceManagementClient(credential, subscription_id)
        storage_client = StorageManagementClient(credential, subscription_id)
        network_client = NetworkManagementClient(credential, subscription_id)
        compute_client = ComputeManagementClient(credential, subscription_id)

        # TC1: Environment active and verified
        tc1_passed = True
        results['tc1'] = tc1_passed
        print("TC1: Environment Verification ......................... [PASSED] (0/0)")

        # Resource configurations
        username = USER_PREFIX.lower().replace('.', '-').replace('@', '-')
        rg_name = f"rg-{username}"
        storage_account_name = f"store{username}".replace('-', '').replace('_', '')[:24]
        vnet_name = f"vnet-{username}"
        nsg_name = f"nsg-{username}"
        vm_name = f"vm-{username}"

        # Check Resource Group
        rg_exists = False
        try:
            resource_client.resource_groups.get(rg_name)
            rg_exists = True
        except Exception:
            pass

        if not rg_exists:
            print("TC2: Storage Account & Container ....................... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Resource Group '{rg_name}' does not exist.")
            print("TC3: Virtual Network & Subnet .......................... [FAILED] (0/5)")
            print("TC4: NSG Inbound Firewall Rules ........................ [FAILED] (0/5)")
            print("TC5: VM Deployment & Specifications .................... [FAILED] (0/5)")
            return

        # TC2: Storage Account + container "assets" exists
        tc2_passed = False
        try:
            sa = storage_client.storage_accounts.get_properties(rg_name, storage_account_name)
            container = storage_client.blob_containers.get(rg_name, storage_account_name, "assets")
            sku_name = sa.sku.name.value if sa.sku else ""
            
            if "Standard_LRS" in sku_name or "Standard" in sku_name:
                tc2_passed = True
                print("TC2: Storage Account & Container ....................... [PASSED] (5/5)")
            else:
                print("TC2: Storage Account & Container ....................... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Sku is expected to be Standard LRS, found '{sku_name}'.")
        except Exception as e:
            print("TC2: Storage Account & Container ....................... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Storage account '{storage_account_name}' or container 'assets' not found. Details: {str(e)}")

        results['tc2'] = tc2_passed
        if tc2_passed:
            total_score += 5

        # TC3: Virtual Network (VNet) + default Subnet config
        tc3_passed = False
        try:
            vnet = network_client.virtual_networks.get(rg_name, vnet_name)
            subnet = network_client.subnets.get(rg_name, vnet_name, "default")
            
            prefixes = vnet.address_space.address_prefixes if vnet.address_space else []
            subnet_prefix = subnet.address_prefix
            
            if "10.0.0.0/16" in prefixes and subnet_prefix == "10.0.0.0/24":
                tc3_passed = True
                print("TC3: Virtual Network & Subnet .......................... [PASSED] (5/5)")
            else:
                print("TC3: Virtual Network & Subnet .......................... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Address Space: {prefixes} (expected ['10.0.0.0/16']), Subnet range: {subnet_prefix} (expected '10.0.0.0/24').")
        except Exception as e:
            print("TC3: Virtual Network & Subnet .......................... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Virtual network '{vnet_name}' or subnet 'default' not found. Details: {str(e)}")

        results['tc3'] = tc3_passed
        if tc3_passed:
            total_score += 5

        # TC4: NSG allowing inbound SSH port 22 exists
        tc4_passed = False
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
                print("TC4: NSG Inbound Firewall Rules ........................ [PASSED] (5/5)")
            else:
                print("TC4: NSG Inbound Firewall Rules ........................ [FAILED] (0/5)")
                print("     └─ [Reason]: No inbound rule allowing TCP/SSH traffic on port 22 found.")
        except Exception as e:
            print("TC4: NSG Inbound Firewall Rules ........................ [FAILED] (0/5)")
            print(f"     └─ [Reason]: Network Security Group '{nsg_name}' not found. Details: {str(e)}")

        results['tc4'] = tc4_passed
        if tc4_passed:
            total_score += 5

        # TC5: Ubuntu VM (Standard_B1s) running and linked
        tc5_passed = False
        try:
            vm = compute_client.virtual_machines.get(rg_name, vm_name, expand='instanceView')
            
            vm_size = vm.hardware_profile.vm_size if vm.hardware_profile else ""
            os_publisher = vm.storage_profile.image_reference.publisher if vm.storage_profile and vm.storage_profile.image_reference else ""
            os_offer = vm.storage_profile.image_reference.offer if vm.storage_profile and vm.storage_profile.image_reference else ""
            
            # Check VM running status
            statuses = [s.code for s in vm.instance_view.statuses] if vm.instance_view else []
            is_running = any("PowerState/running" in status for status in statuses)
            
            is_size_correct = vm_size.lower() in ["standard_b1s"]
            is_ubuntu = "canonical" in os_publisher.lower() and "ubuntu" in os_offer.lower()

            if is_running and is_size_correct and is_ubuntu:
                tc5_passed = True
                print("TC5: VM Deployment & Specifications .................... [PASSED] (5/5)")
            else:
                print("TC5: VM Deployment & Specifications .................... [FAILED] (0/5)")
                print(f"     └─ [Reason]: Size={vm_size} (expected Standard_B1s), OS={os_publisher}/{os_offer} (expected Ubuntu), Running={is_running}")
        except Exception as e:
            print("TC5: VM Deployment & Specifications .................... [FAILED] (0/5)")
            print(f"     └─ [Reason]: Virtual machine '{vm_name}' not found or instance view loading failed. Details: {str(e)}")

        results['tc5'] = tc5_passed
        if tc5_passed:
            total_score += 5

    except Exception as e:
        print(f"[FATAL ERROR] Audit script crashed: {e}")

    # Write test results for local agent evaluation parser
    print(f"\n[SCORE] {total_score}")

if __name__ == '__main__':
    verify_task()
