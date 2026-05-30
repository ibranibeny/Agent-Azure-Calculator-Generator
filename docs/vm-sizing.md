---
layout: default
title: VM Sizing
nav_order: 5
description: "VM SKU selection rules and right-sizing logic."
permalink: /vm-sizing/
---

# VM Sizing Rules
{: .fs-8 }

The agent selects Azure VM SKUs based on a priority system — application type first, then utilization profile, then allocated capacity as fallback.
{: .fs-5 .fw-300 }

---

## Family Selection Priority

### Priority 1: Application Type (Highest)

| Signal | Detected From | VM Family | Rationale |
|--------|--------------|-----------|-----------|
| SQL Server | `sql_detected = Yes` | **E-series** | High memory-to-core ratio |
| Web/IIS | App name contains "IIS", "Web", "HTTP" | **D-series** | Balanced workloads |
| High-CPU batch | App name contains "Batch", "HPC" | **F-series** | CPU-intensive |
| GPU/ML/AI | App name contains "GPU", "ML" | **Manual Review** | Requires NC/ND-series |

### Priority 2: Utilization Profile (Secondary)

| Profile | Condition | VM Family |
|---------|-----------|-----------|
| Memory-heavy | memoryUtil > cpuUtil × 2 | **E-series** |
| CPU-heavy | cpuUtil > memoryUtil × 2 | **F-series** |
| Balanced | Neither condition met | **D-series** |

### Priority 3: Allocated Capacity (Fallback)

If utilization data is unavailable (0%/0%):
- Default to **D-series**
- Use allocated cores/RAM directly (no utilization multiplier)
- Record `sizingMethod: allocated-fallback`

---

## Right-Sizing Formula

```
required_cpu = cpuUtilization × allocatedCores × (1 + buffer/100)
required_ram = memoryUtilization × allocatedRAM_GB × (1 + buffer/100)
```

- **Default buffer**: 20% (configurable at Turn 5)
- Select smallest SKU where `sku.vCPUs >= required_cpu` AND `sku.memoryGB >= required_ram`

---

## Allowed VM Families

| Family | Series | Use Case |
|--------|--------|----------|
| General-purpose | Dv5, Dsv5, Dasv5 | Default, web, app servers |
| Memory-optimized | Ev5, Esv5, Easv5 | SQL, in-memory databases |
| Compute-optimized | Fv2, Fsv2 | Batch processing, high-CPU |

{: .warning }
> **NEVER B-series (burstable)**. Unpredictable performance during migration due to credit-based bursting. D-series is the minimum for all workloads.

---

## Network Architecture

### Hub-and-Spoke Topology

| VNet | CIDR | Purpose |
|------|------|---------|
| Hub | 10.0.0.0/16 | Shared services, firewall, gateway |
| Spoke-Prod | 10.1.0.0/16 | Production workloads |
| Spoke-Dev | 10.2.0.0/16 | Dev/Test workloads |
| Spoke-DMZ | 10.3.0.0/16 | Internet-facing workloads |

### Hub Subnets

| Subnet | CIDR | Requirement |
|--------|------|-------------|
| AzureFirewallSubnet | /26 minimum | Required name |
| GatewaySubnet | /27 minimum | Required for VPN/ER |
| AzureBastionSubnet | /26 minimum | Required for Bastion |
| SharedServices | /24 | AD DS, DNS, monitoring |

### Spoke Subnets (per spoke)

| Subnet | CIDR | Tier |
|--------|------|------|
| web-subnet | /24 | Frontend / load balancers |
| app-subnet | /24 | Application servers |
| data-subnet | /24 | Database servers |

---

## Infrastructure Server Detection

Servers matching these patterns are placed in the **hub SharedServices subnet** (not in spokes):

| Pattern | Infrastructure Role |
|---------|-------------------|
| Active Directory, AD DS, DC | Identity/Auth |
| DNS, BIND | Name Resolution |
| SCCM, ConfigMgr | Configuration Management |
| WSUS | Patch Management |
| SCOM, Monitoring | Monitoring |
| Backup, Veeam | Backup/DR |
| Print Server | Print Services |
| Certificate Authority, PKI | Security |
| File Server, DFS | Shared Storage |
