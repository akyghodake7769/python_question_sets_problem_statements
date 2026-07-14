# Azure Lab: Azure Virtual Machine & Security Configuration

Duration : 60 Min.

## Scenario

As a DevOps Engineer at LabsKraft, you are tasked with provisioning a secure hosting environment in Microsoft Azure. Your objective is to deploy an Ubuntu virtual machine, configure network settings with appropriate security rules using a Network Security Group (NSG), and verify that the virtual machine is deployed, configured, and actively running.

## Input Details

The environment has been pre-configured with the following resources:

- **Subscription:** LabsKraft
- **Resource Group:** `rg-iRUN-LTM-Assessment`
- **Region:** Asia Pacific East Asia (use `eastasia` region)

## Username & Naming Conventions

Your candidate prefix is the part of your Azure login email before the `@` symbol.
For example, if your Azure username is `ltmdemo01@michaelkloudkrafthotmail.onmicrosoft.com`, your prefix is **`ltmdemo01`**.

You must name your resources accordingly:

- **Virtual Network Name:** `vnet-<prefix>` (e.g. `vnet-ltmdemo01`)
- **Network Security Group Name:** `nsg-<prefix>` (e.g. `nsg-ltmdemo01`)
- **Virtual Machine Name:** `vm-<prefix>` (e.g. `vm-ltmdemo01`)

## Task Objectives

Perform the following configuration steps directly in the Azure Portal or using the Azure CLI:

### 1. Configure Networking

- **Virtual Network Name:** `vnet-<prefix>`
- **Resource Group:** Use the pre-existing Resource Group `rg-iRUN-LTM-Assessment`.
- **Location:** Deploy the VNet in the `eastasia` region.
- **Address Space:** `10.0.0.0/16`
- **Subnet Name:** `default` (Subnet address range: `10.0.0.0/24`)

### 2. Network Security Configuration

- **Network Security Group Name:** `nsg-<prefix>`
- **SSH Rule:** Create an inbound security rule to allow SSH traffic:
  - **Protocol:** TCP
  - **Destination Port Ranges:** `22`
  - **Source:** Any (`*`)
  - **Action:** Allow

### 3. Deploy Virtual Machine

- **Virtual Machine Name:** `vm-<prefix>`
- **Size:** `Standard_B1s`
- **Operating System:** Ubuntu Server 22.04 LTS
- **Security:** Configure SSH key-based authentication for the administrator account. Ensure password-based authentication is explicitly disabled for enhanced SSH security.
- **Network Association:** Associate the VM's network interface with `vnet-<prefix>`, subnet `default`, and bind it to the Network Security Group `nsg-<prefix>`. The VM must be in a running state.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score. The verification system will check the actual resources in the Azure cloud.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                                                          | Marks   |
| ------------- | ---------------------------------------------------------------------------------------------------- | ------- |
| **TC1** | Resource Group validation (`rg-iRUN-LTM-Assessment` exists and is accessible)                      | 0 Marks |
| **TC2** | Virtual Network (`vnet-<prefix>` 10.0.0.0/16) and subnet default (`10.0.0.0/24`) in `eastasia` | 4 Marks |
| **TC3** | NSG (`nsg-<prefix>`) exists and is associated                                                      | 4 Marks |
| **TC4** | NSG rules check (Inbound SSH traffic allowed on Port 22)                                             | 4 Marks |
| **TC5** | Ubuntu VM (`vm-<prefix>` Standard_B1s) is deployed and running                                     | 4 Marks |
| **TC6** | VM Authentication Security (Password authentication is disabled, requiring SSH key pairs)            | 4 Marks |

**Total Score: 20 Marks**

## Important Notes

- Ensure all resource names contain your candidate username prefix in lowercase.
- The VM must be actively running during evaluation.
