---
description: "Use when mapping on-premises servers to Azure VM SKUs, selecting VM families based on application type, right-sizing based on utilization, or applying buffer calculations."
applyTo: "**"
---

# VM SKU Selection Logic

## Family Selection Priority

Select the VM family based on this priority order:

### Priority 1: Application Type (highest)

| Signal | Detected From | VM Family | Rationale |
|--------|--------------|-----------|-----------|
| SQL Server detected | `sqlDetected = Yes` | **E-series** (memory-optimized) | SQL needs high memory-to-core ratio |
| Web/IIS application | applicationName contains "IIS", "Web", "HTTP", "Apache", "Nginx" | **D-series** (general-purpose) | Balanced workloads |
| High-CPU batch/compute | applicationName contains "Batch", "Render", "HPC", "Compute" | **F-series** (compute-optimized) | CPU-intensive tasks |
| GPU/ML/AI | applicationName contains "GPU", "ML", "AI", "CUDA", "Rendering" | **Manual Review** | Requires NC/ND-series — flag for human |

### Priority 2: Utilization Profile (secondary)

If no application type signal is detected:

| Profile | Condition | VM Family |
|---------|-----------|-----------|
| Memory-heavy | memoryUtilization > cpuUtilization × 2 | **E-series** |
| CPU-heavy | cpuUtilization > memoryUtilization × 2 | **F-series** |
| Balanced | Neither condition met | **D-series** |

### Priority 3: Allocated Capacity (fallback)

If utilization data is unavailable (0%/0%) or unreliable:
- Default to **D-series** (general-purpose)
- Use allocated capacity (cores/RAM) as sizing input

## NO B-SERIES POLICY

**NEVER recommend B-series (burstable) VMs.** Use D-series as the minimum for ALL workloads including:
- Low-utilization servers
- Development/Test environments
- Infrastructure services

Rationale: B-series has unpredictable performance due to credit-based bursting.

## Right-Sizing Calculation

```
required_cpu = cpuUtilization × allocatedCores × (1 + buffer/100)
required_ram = memoryUtilization × allocatedRAM_GB × (1 + buffer/100)
```

- Default buffer: **20%** (user-configurable)
- Find the smallest Azure SKU in the selected family where:
  - `sku.vCPUs >= required_cpu`
  - `sku.memoryGB >= required_ram`

### Zero Utilization Handling

If cpuUtilization = 0% AND memoryUtilization = 0%:
- Treat as **monitoring gap** (not idle server)
- Fall back to allocated capacity
- Record `sizingMethod: allocated-fallback`

### GPU/HPC Flagging

If GPU/HPC patterns detected:
- Mark as `sizingMethod: manual-review`
- Exclude from auto-sizing
- Note: "Requires NC/ND/NV-series evaluation"

## Allowed VM Families

| Family | Series | Use Case |
|--------|--------|----------|
| General-purpose | D-series (Dv5, Dsv5, Dasv5) | Default, web, app servers |
| Memory-optimized | E-series (Ev5, Esv5, Easv5) | SQL, in-memory databases, analytics |
| Compute-optimized | F-series (Fv2, Fsv2) | Batch processing, high-CPU workloads |

Prefer latest generation (v5). Fall back to v4 if v5 unavailable in region.

## Sizing Output Format

| Field | Value |
|-------|-------|
| skuFamily | D / E / F |
| familyRationale | "SQL detected → memory-optimized" |
| skuName | "Standard_E4s_v5" |
| vCPUs | 4 |
| memoryGB | 32 |
| sizingMethod | right-sized / allocated-fallback / manual-review |
| availabilityConfirmed | true / false |
