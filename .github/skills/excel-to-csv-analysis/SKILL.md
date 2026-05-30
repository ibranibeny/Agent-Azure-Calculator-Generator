---
name: excel-to-csv-analysis
description: "Analyze App-to-Server Export and Rightsizing Disks sheet, correlate by server name, and generate a consolidated CSV report. Use when: creating a unified server inventory CSV, correlating server metadata with disk specs, preparing input for Azure Calculator automation."
argument-hint: "Provide full Windows paths to both .xlsx files (Rightsizing Export and App-to-Server Export)"
---

# Excel Analysis → CSV Report Generation

## When to Use

- Building a consolidated server report merging application metadata with disk storage specs
- Preparing a clean CSV input file for Azure Pricing Calculator automation
- Creating a portable report combining: server, application, environment, OS, power status, SQL detection, treatment, and disk details

## CSV Output Schema

One row per **server-disk combination** (a server with 3 disks = 3 rows):

```csv
server_name,application_name,environment,os_version,power_status,sql_detected,treatment,recommended_sku,vm_family,disk_name,disk_size_gb,disk_iops,disk_throughput_mbps
```

| Column | Source | Description |
|--------|--------|-------------|
| `server_name` | App-to-Server col A | Hostname |
| `application_name` | App-to-Server col C | Workload group |
| `environment` | App-to-Server col D | Prod / Dev / UAT |
| `os_version` | App-to-Server col I | Full OS string |
| `power_status` | App-to-Server col H | On / Off |
| `sql_detected` | App-to-Server col K | Yes / No |
| `treatment` | App-to-Server col E | 6R suggestion |
| `recommended_sku` | Agent-derived | Azure VM SKU (populated during sizing) |
| `vm_family` | Agent-derived | D / E / F family |
| `disk_name` | Disks col B | Disk identifier |
| `disk_size_gb` | Disks col C | Disk capacity in GB |
| `disk_iops` | Disks col D | IOPS |
| `disk_throughput_mbps` | Disks col E | Throughput MB/s |

## Procedure

### Step 1: Open App-to-Server Export
### Step 2: Read App-to-Server List Sheet (headers at row 4)
### Step 3: Close App-to-Server Export
### Step 4: Open Rightsizing Export
### Step 5: Read Disks Sheet (headers at row 6)
### Step 6: Close Rightsizing Export
### Step 7: Correlate Data

Build lookup from App-to-Server keyed by server name (case-insensitive):
- Match found → merge metadata + disk data
- No match → include with empty metadata, flag as unmatched
- Server with no disks → one row with empty disk columns

### Step 8: Deduplicate Servers

- Use first occurrence for OS, environment, power status
- If `sql_detected = Yes` on ANY row → set Yes
- Comma-separate multiple application names

### Step 9: Generate CSV File

Write to: `output/migration-plan/<customer-name>-server-inventory.csv`

### Step 10: Report Summary

```
✅ CSV generated: output/migration-plan/<customer>-server-inventory.csv

Summary:
- Total servers: N
- Total disks: M
- Servers with disk data: X
- Servers without disk data: Y (metadata only)
- Disks without server match: Z (orphaned)
```

## Accuracy Validation (FR-035)

After CSV generation, validate against source Excel:

| Metric | Formula | Threshold |
|--------|---------|-----------|
| Server Coverage % | (unique servers in CSV / unique servers in source) × 100 | ≥ 99% |
| Disk Coverage % | (disk rows in CSV / disk rows in source) × 100 | ≥ 95% |
| Field Accuracy % | (correct field values / total fields checked) × 100 | ≥ 98% |

## Error Handling

| Error | Action |
|-------|--------|
| Sheet not found | Try alternate names; abort if none found |
| IRM-protected | Re-open with show=true |
| Empty sheet | Report "0 rows found" — continue |
| Column mismatch | Report missing, attempt best-effort |
| Server name mismatch | Normalize: trim, case-insensitive, strip domain |
