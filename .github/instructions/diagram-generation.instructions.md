---
description: "Use when generating hub-and-spoke network topology diagrams using the Python Diagrams library, including output path conventions and required infrastructure icons."
applyTo: "**"
---

# Diagram Generation Conventions

## Library: Python Diagrams

Use the [diagrams](https://diagrams.mingrammer.com/) library (requires Graphviz installed).

## Required Code Pattern

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import VirtualNetworks, Firewall, VPNGateways, ApplicationGateway
from diagrams.azure.compute import VM
from diagrams.azure.security import KeyVaults
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.general import Subscriptions

with Diagram(
    "{customer_name} - Hub and Spoke Architecture",
    filename="{output_path}/architecture/{customer_name}_hub_spoke",
    show=False,
    direction="TB",
    graph_attr={"fontsize": "12", "bgcolor": "white"}
):
    # Hub VNet cluster
    with Cluster("Hub VNet (10.0.0.0/16)"):
        fw = Firewall("Azure Firewall")
        gw = VPNGateways("VPN/ER Gateway")
        with Cluster("SharedServices"):
            infra_vms = [VM(name) for name in infrastructure_servers]

    # Spoke clusters (one per workload group)
    for spoke in spokes:
        with Cluster(f"Spoke: {spoke.name} ({spoke.cidr})"):
            with Cluster("app-subnet"):
                app_vms = [VM(name) for name in spoke.app_servers]
            with Cluster("data-subnet"):
                data_vms = [VM(name) for name in spoke.data_servers]

    # Peering connections
    for spoke_cluster in spoke_clusters:
        spoke_cluster >> Edge(label="peering") >> fw
```

## Output Path Convention

```
output/{customer_name}/architecture/{customer_name}_hub_spoke.png
```

- Format: PNG (default), also generate SVG if user requests
- Filename uses snake_case with customer prefix

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Diagram title | "{Customer} - Hub and Spoke Architecture" | "Contoso - Hub and Spoke Architecture" |
| Hub cluster | "Hub VNet ({cidr})" | "Hub VNet (10.0.0.0/16)" |
| Spoke cluster | "Spoke: {group_name} ({cidr})" | "Spoke: Finance-Prod (10.1.0.0/16)" |
| VM nodes | Server hostname (truncated to 15 chars) | "SQLPROD01" |

## Diagram Content Rules

1. Show all spokes — one cluster per workload group
2. Show infrastructure servers in hub SharedServices subnet
3. Show peering — edges from each spoke to hub firewall
4. Show subnet tiers — web/app/data (only if servers exist in that tier)
5. Limit VM nodes — if >8 servers, show first 5 + "... +N more" label

## Dependencies

- `pip install diagrams` (Python 3.6+)
- Graphviz must be installed (`apt install graphviz` or `brew install graphviz`)
- The agent outputs a Python script for the user to run
