---
name: csv-source-reconciliation
description: "Mandatory pre-gate: validate CSV output against source Excel file(s) line-by-line before proceeding to Azure Calculator or final report. Compares total row count, server names, disk entries, and field values 1:1. Use when: CSV generated, before Calculator automation, before delivering assessment."
argument-hint: "Provide paths to: (1) source Excel file(s), (2) generated CSV file"
---

# CSV-to-Source Reconciliation Gate

## Purpose

This skill is a **MANDATORY gate** that runs immediately after CSV generation and BEFORE:
- Azure Calculator automation (calculator-from-csv skill)
- Final assessment report delivery

It performs a **line-by-line reconciliation** between source Excel and generated CSV to guarantee data fidelity.

## When to Run

1. After `excel-to-csv-analysis` skill generates the CSV
2. Before `calculator-from-csv` or `azure-calculator-automation` skill is invoked
3. On user request ("validate", "check", "reconcile")

## Gate Pass Criteria

ALL must be true to pass:

| Check | Condition | Fail Action |
|-------|-----------|-------------|
| Server count match | CSV unique servers == Excel unique servers (in-scope) | BLOCK — re-run CSV |
| Row count match | CSV total rows == expected (servers × disks) | WARN — report discrepancy |
| No missing servers | Every in-scope server in Excel exists in CSV | BLOCK — list missing |
| No extra servers | Every server in CSV exists in Excel | WARN — list extras |
| Field value match | Spot-check passes ≥98% accuracy | WARN — list mismatches |

## Procedure

### Step 1: Establish Ground Truth from Excel

#### Single-File Mode
- Open source Excel, scan sheets
- Count total data rows (excluding headers)
- Extract server names and disk data
- Build ground truth lists

#### Two-File Mode
- Open Rightsizing Export → read Servers sheet (headers at row 6)
- Filter only "In Scope" servers (col C)
- Read Disks sheet → count disk rows
- Open App-to-Server Export → cross-reference

### Step 2: Load CSV and Count

```bash
# Count unique servers
cut -d',' -f1 output/migration-plan/<customer>-server-inventory.csv | sort -u | wc -l

# Count total rows (excluding header)
tail -n +2 output/migration-plan/<customer>-server-inventory.csv | wc -l
```

### Step 3: Compare Server Names

```
For each server in ground_truth_servers:
  if server NOT in csv_servers:
    missing_servers.append(server)

For each server in csv_servers:
  if server NOT in ground_truth_servers:
    extra_servers.append(server)
```

### Step 4: Compare Disk Entries

```
For each disk in ground_truth_disks:
  if (disk.server, disk.name) NOT in csv_disks:
    missing_disks.append(disk)
```

### Step 5: Spot-Check Field Values

Select 10 random servers and verify:
- server_name matches exactly
- disk_size_gb matches source
- os_version matches source
- sql_detected matches source

### Step 6: Report Gate Result

```
## Reconciliation Gate Result: [PASS / WARN / FAIL]

| Check | Result | Details |
|-------|--------|---------|
| Server Count | ✅/❌ | Excel: N, CSV: M |
| Row Count | ✅/⚠️ | Expected: X, Actual: Y |
| Missing Servers | ✅/❌ | [count] missing |
| Extra Servers | ✅/⚠️ | [count] extra |
| Field Accuracy | ✅/⚠️ | XX% (N/M correct) |

[If FAIL]: ❌ BLOCKED — Cannot proceed to Calculator. Fix CSV generation.
[If WARN]: ⚠️ Proceeding with noted discrepancies.
[If PASS]: ✅ Gate passed — safe to proceed to Calculator automation.
```

## MCP Tools Used

- `mcp_excel-mcp_file` — Open/close Excel for ground truth extraction
- `mcp_excel-mcp_range` — Read cell values
- `mcp_excel-mcp_worksheet` — List sheets
