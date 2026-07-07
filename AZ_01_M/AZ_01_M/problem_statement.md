# Azure Cloud Assessment: Virtual Machine & Storage Setup

**Duration:** 60 Minutes  
**Total Marks:** 20 Marks  

## Objectives

Configure a basic, secure hosting environment in Microsoft Azure. All resource names must contain your candidate username prefix (referred to as `<username>` below, which is the prefix of your candidate username, e.g., if username is `labs-demo-user1`, then use `labs-demo-user1`) to ensure uniqueness.

You must perform the following tasks directly in the Azure Portal or using the Azure CLI:

---

### Task 1: Create Resource Group & Storage Account (5 Marks)
* **Resource Group Name**: `rg-<username>` (e.g., `rg-labs-demo-user1`)
* **Storage Account Name**: `store<username>` (Important: Storage Account names must be between 3 and 24 characters, use numbers and lowercase letters only, and no special characters. E.g., if username is `labs-demo-user1`, use `storelabsdemouser1` or similar truncated format, ensuring it starts with `store` followed by your username, stripped of all hyphens/underscores/special characters, max 24 characters).
* **Storage Account Tier/Sku**: Standard LRS (`Standard_LRS`).
* **Blob Container**: Inside this storage account, create a private container named `assets`.

### Task 2: Configure Networking (5 Marks)
* **Virtual Network Name**: `vnet-<username>`
* **Address Space**: `10.0.0.0/16`
* **Subnet Name**: `default` (Subnet address range: `10.0.0.0/24`)

### Task 3: Network Security Configuration (5 Marks)
* **Network Security Group (NSG) Name**: `nsg-<username>`
* **Security Rules**: Create an inbound security rule to allow SSH traffic:
  * **Protocol**: TCP
  * **Destination Port Ranges**: `22`
  * **Source**: Any (`*`)
  * **Action**: Allow
  * **Priority**: 1000 (or any valid priority)

### Task 4: Deploy Virtual Machine (5 Marks)
* **Virtual Machine Name**: `vm-<username>`
* **Size**: `Standard_B1s`
* **Operating System**: Ubuntu Server 22.04 LTS
* **Networking**: Associate the VM's network interface with `vnet-<username>`, subnet `default`, and bind it to the Network Security Group `nsg-<username>`.
* **VM Power State**: The VM must be in a running state.

---

## Verification

Click the **Run Tests** button in the KodeArena application to verify your configuration. The evaluation script will audit your Azure resources in real-time.
