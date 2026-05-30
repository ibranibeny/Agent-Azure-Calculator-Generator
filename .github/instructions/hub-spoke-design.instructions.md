---
description: "Use when designing Azure hub-and-spoke network topologies, VNet peering, Azure Firewall routing, or network segmentation for migration workloads."
applyTo: "**"
---

# Hub-and-Spoke Network Design Principles

## Architecture Rules

1. **Single Hub per Region** — One hub VNet per Azure region containing all shared services
2. **Spoke Isolation** — Spokes cannot communicate directly; all inter-spoke traffic routes through the hub firewall
3. **Gateway Transit** — Enable gateway transit on hub peering so spokes use the hub's VPN/ExpressRoute gateway
4. **UDR on Spokes** — Every spoke subnet has a User Defined Route sending 0.0.0.0/0 to Azure Firewall private IP
5. **DNS Resolution** — Use Azure Private DNS Zones linked to hub; spokes use hub DNS forwarder

## 6R Decision Tree

```
Is the workload still needed?
├── No → RETIRE
└── Yes → Is there a SaaS replacement?
    ├── Yes, and acceptable → REPLACE
    └── No → Can it run as-is on Azure VM?
        ├── Yes, minimal risk → REHOST
        └── Partially → Can minor PaaS swaps help?
            ├── Yes (e.g., managed DB) → REPLATFORM
            └── No → Is the codebase maintainable?
                ├── Yes → REFACTOR
                └── No → REBUILD
```

## CIDR Allocation Rules

| VNet | CIDR | Purpose |
|------|------|---------|
| Hub | 10.0.0.0/16 | Shared services, firewall, gateway |
| Spoke-Prod | 10.1.0.0/16 | Production workloads |
| Spoke-Dev | 10.2.0.0/16 | Dev/Test workloads |
| Spoke-DMZ | 10.3.0.0/16 | Internet-facing workloads |
| Spoke-Data | 10.4.0.0/16 | Databases, storage (if separate) |

Hub Subnet allocation:
| Subnet | CIDR | Requirement |
|--------|------|-------------|
| AzureFirewallSubnet | /26 minimum | Required name, Azure-managed |
| GatewaySubnet | /27 minimum | Required name for VPN/ER |
| AzureBastionSubnet | /26 minimum | Required name for Bastion |
| SharedServices | /24 | AD DS, DNS forwarders, monitoring |

Spoke Subnet allocation (per spoke):
| Subnet | CIDR | Tier |
|--------|------|------|
| web-subnet | /24 | Frontend / load balancers |
| app-subnet | /24 | Application servers |
| data-subnet | /24 | Database servers |

## Spoke Segmentation Options

1. **By Environment** — Production, Dev/Test, Staging (most common for lift-and-shift)
2. **By Business Unit** — Finance, HR, Engineering (org-driven isolation)
3. **By Application** — One spoke per application group (maximum isolation)
4. **By Compliance** — PCI, HIPAA, general (regulatory-driven)

## Network Security Rules

- NSGs on every subnet (deny-all inbound by default)
- Application Security Groups for logical server grouping
- Azure Firewall DNAT rules for inbound from on-premises
- Azure Firewall Network Rules for spoke-to-spoke (when allowed)
- No public IPs on spoke VMs (all access via Bastion or VPN)

## Infrastructure Server Detection

Infrastructure servers belong in the **hub SharedServices subnet**, NOT in spoke VNets:

| Pattern (case-insensitive) | Infrastructure Role |
|---------------------------|---------------------|
| "Active Directory", "AD DS", "Domain Controller" | Identity/Auth |
| "DNS", "BIND" | Name Resolution |
| "SCCM", "ConfigMgr", "MECM" | Configuration Management |
| "WSUS", "Windows Update" | Patch Management |
| "SCOM", "Monitoring", "Nagios", "Zabbix" | Monitoring |
| "Backup", "Veeam", "Commvault" | Backup/DR |
| "DHCP" | Network Services |
| "Certificate Authority", "PKI" | Security/PKI |
| "File Server", "DFS" | Shared Storage |

### Placement Rules

1. Detected infrastructure servers → hub `SharedServicesSubnet`
2. EXCLUDED from spoke VM counts
3. Included in hub cost calculations
4. Present to user for confirmation before finalizing
