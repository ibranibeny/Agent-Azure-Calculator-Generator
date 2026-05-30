---
name: azure-cost-availability
description: "Check Azure service pricing and regional SKU availability. Use when: estimating migration costs, verifying VM SKU availability in a region, comparing pricing tiers (pay-as-you-go vs reserved), checking disk type availability (Premium SSD, Standard SSD, Standard HDD), validating service availability by region."
argument-hint: "Specify the Azure service, SKU, or region to check pricing/availability"
---

# Azure Cost and Service Availability

## When to Use

- Checking if a specific VM SKU is available in a target Azure region
- Getting real-time pricing for Azure VMs, storage, networking
- Comparing pay-as-you-go vs 1-year vs 3-year reserved instance pricing
- Verifying disk type availability per region
- Checking Azure Firewall, VPN Gateway, or other networking service pricing
- Validating that all recommended services exist in the target region

## Procedure

### 1. Identify what to check
- VM SKU availability → Azure MCP compute/pricing tools
- Pricing comparison → Azure MCP pricing tool
- Service availability → Azure MCP resource/region tools

### 2. Check SKU availability in region
- Query Azure MCP for available VM sizes in the target region
- Filter by required vCPU count, memory, and disk capabilities
- Flag any requested SKUs that are unavailable or restricted

### 3. Fetch real-time pricing
- Use Azure MCP pricing tool with filters: region, VM series, OS type
- Include compute hours, managed disk costs, and bandwidth
- Calculate monthly estimate (730 hours/month for always-on)

### 4. Compare pricing tiers

| Tier | Use Case | Savings |
|------|----------|---------|
| Pay-as-you-go | Dev/Test, variable workloads | Baseline |
| 1-year Reserved | Stable prod workloads | ~30-40% savings |
| 3-year Reserved | Long-term committed workloads | ~50-60% savings |
| Spot | Fault-tolerant batch jobs | ~60-90% savings |
| Dev/Test pricing | Non-prod with VS subscription | ~40% savings |

### 5. Environment-specific disk recommendations

| Environment | Recommended Disk | Rationale |
|-------------|-----------------|-----------|
| Production | Premium SSD (P30+) | IOPS guarantee, SLA backing |
| Production (cost-sensitive) | Standard SSD | Good performance, lower cost |
| Development/Test | Standard HDD | Lowest cost, acceptable for non-critical |
| High-performance | Ultra Disk | Sub-ms latency, high IOPS |

### 6. Return structured pricing result

```
## Azure Pricing: [Resource Type]

**Region**: [Selected Region]
**Environment**: Production / Development

| Resource | SKU | Monthly (PAYG) | Monthly (1yr RI) | Monthly (3yr RI) |
|----------|-----|----------------|------------------|------------------|
| [VM]     | [SKU] | $X,XXX | $X,XXX | $X,XXX |

**Disk Storage**:
| Disk Type | Size | Monthly Cost |
|-----------|------|-------------|
| [Type]    | [GB] | $XX         |

**Total Monthly Estimate**: $X,XXX
**Total Annual Estimate**: $XX,XXX
```

## SKU Availability Verification

Before recommending any VM SKU, verify availability in the target region:

1. Query `mcp_azure_mcp_compute` for available VM sizes
2. Filter by required minimum vCPUs and memory
3. Confirm recommended SKU appears in available list
4. If confirmed: mark `availabilityConfirmed: true`
5. If NOT available: trigger fallback logic

### Fallback for Unavailable SKUs

1. **Same series, different size**: Try next-larger SKU (e.g., D4s_v5 → D8s_v5)
2. **Same generation, different series**: Try equivalent (e.g., D4s_v5 → E4s_v5)
3. **Previous generation**: Try v4 series (e.g., D4s_v5 → D4s_v4)
4. **Alternative region**: Suggest nearest region with availability

Report fallback:
```
⚠️ SKU Unavailable: Standard_D8s_v5 is not available in westus2.
   Recommendation: Standard_D8s_v4 (previous gen, available in westus2)
   Alternative: Standard_D8s_v5 is available in westus3 (+2ms latency)
```

## MCP Tools Used

- `mcp_azure_mcp_pricing` — Real-time pricing queries
- `mcp_azure_mcp_compute` — VM SKU availability and specs
