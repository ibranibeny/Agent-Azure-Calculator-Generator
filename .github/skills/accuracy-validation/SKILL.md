---
name: accuracy-validation
description: "Validate the accuracy of generated CSV and Azure Calculator output against the original Excel source files as ground truth. Use when: verifying data integrity after CSV generation, confirming no servers or disks were lost during correlation, spot-checking field values against source, calculating accuracy metrics."
argument-hint: "Provide paths to: (1) source Excel file(s), (2) generated CSV file"
---

# Accuracy Validation — CSV/Calculator vs Excel Ground Truth

## When to Use

- After generating the consolidated CSV to verify data completeness
- After Azure Calculator automation to confirm all resources were added
- When the user requests a data integrity check
- As the final quality gate before delivering the migration assessment

## Accuracy Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Server Coverage %** | Unique servers in CSV ÷ Unique servers in source Excel × 100 | ≥ 99% |
| **Disk Coverage %** | Disk rows in CSV ÷ Disk rows in source Excel × 100 | ≥ 95% |
| **Field Accuracy %** | Correct field values ÷ Total fields spot-checked × 100 | ≥ 98% |

**Overall Accuracy Score** = (Server Coverage × 0.4) + (Disk Coverage × 0.3) + (Field Accuracy × 0.3)

## Procedure

### Step 1: Load Source Excel — Count Ground Truth

Open source Excel via Excel MCP and extract baseline counts:
- Total server count (unique hostnames)
- Server name list (for name-by-name comparison)
- Total disk count
- Disk-to-server mapping

### Step 2: Load Generated CSV — Count Output

Read CSV and extract:
- Unique server names
- Total rows
- Unique disk entries (server_name + disk_name pairs)

### Step 3: Calculate Server Coverage

```
server_coverage = (unique_servers_in_csv / unique_servers_in_excel) × 100
Missing servers = servers in Excel NOT found in CSV
Extra servers = servers in CSV NOT found in Excel (should be 0)
```

### Step 4: Calculate Disk Coverage

```
disk_coverage = (disk_rows_in_csv / disk_rows_in_excel) × 100
Missing disks = disk entries in Excel NOT found in CSV
```

### Step 5: Calculate Field Accuracy (Spot Check)

Select sample (all if ≤50 servers, random 50 if >50) and validate:

| Field | CSV Column | Excel Source |
|-------|-----------|--------------|
| `server_name` | col 1 | Rightsizing Servers col A |
| `disk_size_gb` | col 11 | Rightsizing Disks col C |
| `os_version` | col 4 | App-to-Server col I |
| `sql_detected` | col 6 | App-to-Server col K |
| `application_name` | col 2 | App-to-Server col C |

### Step 6: Report Results

```
## Accuracy Validation Report

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Server Coverage | XX% | ≥99% | ✅/❌ |
| Disk Coverage | XX% | ≥95% | ✅/❌ |
| Field Accuracy | XX% | ≥98% | ✅/❌ |
| Overall Score | XX% | ≥97% | ✅/❌ |

Missing Servers: [list or "None"]
Missing Disks: [list or "None"]
Field Mismatches: [list or "None"]
```

## Gate Decision

- **PASS** (all metrics meet targets): Proceed to next step
- **WARN** (one metric below target): Report to user, proceed with caution
- **FAIL** (server coverage < 99%): BLOCK — re-run CSV generation
