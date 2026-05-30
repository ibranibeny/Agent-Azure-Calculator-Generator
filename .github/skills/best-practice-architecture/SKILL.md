---
name: best-practice-architecture
description: "Validate Azure architecture designs against Microsoft Learn best practices. Use when: designing hub-and-spoke topology, validating network segmentation, checking VM placement, verifying firewall rules, reviewing migration methodology, confirming Well-Architected Framework alignment."
argument-hint: "Describe the architecture pattern or design decision to validate"
---

# Best Practice Architecture Validation

## When to Use

- Validating hub-and-spoke network design decisions
- Checking if a proposed architecture aligns with Cloud Adoption Framework
- Verifying network security best practices (NSGs, Firewall, Private Endpoints)
- Confirming migration methodology alignment (Azure Migrate best practices)
- Reviewing Well-Architected Framework pillars

## Procedure

1. **Identify the architecture decision** to validate
2. **Search Microsoft Learn documentation** using MCP tools
3. **Cross-reference with Well-Architected Framework**
4. **Validate against Cloud Adoption Framework**
5. **Return structured validation result**:

```
## Validation: [Design Decision]

**Status**: ✅ Aligned / ⚠️ Partially Aligned / ❌ Misaligned

**Microsoft Learn Reference**: [URL]

**Findings**:
- [What aligns with best practices]
- [What deviates and why it matters]

**Recommendations**:
- [Specific changes to align with best practices]
```

## Reference Patterns

### Hub-and-Spoke Validation Checks
- Single hub per region with shared services
- Spoke isolation (no direct spoke-to-spoke)
- Gateway transit enabled on peering
- UDR 0.0.0.0/0 → Azure Firewall on all spoke subnets
- Azure Private DNS Zones linked to hub
- Bastion in hub for management access

### Security Validation Checks
- No public IPs on workload VMs
- NSGs on every subnet
- Azure Firewall for east-west and north-south traffic
- Private Endpoints for all PaaS services
- Key Vault for secrets management
- Microsoft Defender for Cloud enabled

### Migration Methodology Checks
- Assessment before migration (Azure Migrate)
- Phased wave approach (not big-bang)
- Dependency mapping completed
- Rollback plan documented per wave
- Post-migration validation criteria defined

### VM SKU Validation
- Selected SKU family appropriate for workload type
- SKU available in target region
- No B-series for production
- Memory-to-CPU ratio matches workload profile

### Network Design Validation
- Hub-spoke follows 5 Architecture Rules
- CIDR ranges don't overlap with on-premises
- Subnet sizing supports growth (>50% = warning)
- Firewall subnet at least /26
- GatewaySubnet at least /27

### Security Posture Validation
- All spoke VMs have no public IPs
- NSG on every subnet
- Firewall rules follow least-privilege

## MCP Tools Used

- `microsoft_docs_search` — Search for architecture best practices
- `microsoft_docs_fetch` — Fetch full documentation for detailed guidance
- `microsoft_code_sample_search` — Find reference implementation examples
