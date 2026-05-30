---
name: excel-data-ingestion
description: "Parse Azure Rightsizing Export and App-to-Server Export Excel files via Excel MCP tools. Use when: importing server inventory from Excel, reading Servers/Disks/App-to-Server sheets, correlating server-to-disk-to-OS data, extracting on-premises specs for migration assessment."
argument-hint: "Provide full Windows paths to both .xlsx files (Rightsizing Export and App-to-Server Export)"
---

# Excel Data Ingestion (Two-File and Single-File Migration Assessment)

## When to Use

- Importing server inventory from Azure Rightsizing Export (.xlsx) and App-to-Server Export (.xlsx)
- Reading the Servers sheet for compute specs (CPU, RAM, storage, utilization)
- Reading the Disks sheet for storage metrics (size, IOPS, throughput)
- Reading the App-to-Server List sheet for OS versions, application mapping, and 6R treatment suggestions
- Correlating servers to their associated disks and OS metadata
- Extracting workload groupings from "Associated Apps" and "Scope" columns

## Input Files

### Two-File Mode

Requires **two Excel files**:

| # | File | Key Data |
|---|------|----------|
| 1 | **Azure Rightsizing Export** | Server specs (CPU, RAM, utilization), Disk metrics (IOPS, throughput) |
| 2 | **App-to-Server Export** | Application name, OS version, environment, power status, 6R treatment |

Both files use the **Application Name** as the join key:
- Rightsizing Export "Associated Apps" (col D) == App-to-Server Export "Application Name" (col C)

### Single-File Mode

When the user provides **one** Excel file, the agent enters single-file mode:
- Scan all sheets, fuzzy-match columns
- Present column mapping confirmation report
- Handle comma-delimited disk data in single cells

## Two-File Procedure

### Step 1: Open the Rightsizing Export

```
Tool: mcp_excel-mcp_file
Action: open
Path: <user-provided .xlsx path>
Show: true (file may be IRM/AIP protected — requires interactive session)
Timeout: 180
```

### Step 2: Identify Sheets

```
Tool: mcp_excel-mcp_worksheet
Action: list
```

Expected sheets: "Servers" (compute data) and "Disks" (storage data).

### Step 3: Read Metadata (Rows 2-3)

```
Tool: mcp_excel-mcp_range
Action: get-values
Sheet: Servers
Range: A2:B3
```

Extract Customer name and Currency for the report header.

### Step 4: Read Servers Sheet Headers and Data

```
Tool: mcp_excel-mcp_range
Action: get-values
Sheet: Servers
Range: A6:AE6   (headers)
```

**Format Validation (fail-fast)**: After reading row 6 headers, verify these required columns exist:
- "Server" (or "Machine Name") — column A
- "Current Cores" — column G
- "Current CPU Usage (%)" — column H
- "Current RAM (MB)" — column I
- "Current Memory Usage (%)" — column J
- "Storage (GB)" — column K

If ANY required column is missing:
- **ABORT** immediately
- Report: "❌ Format validation failed: Missing required column(s): [list]. Please verify the correct file was provided."

Then read data rows: `Range: A7:AE<last_row>`

#### Servers Sheet — Input Columns (USE these)

| Column | Header | Purpose |
|--------|--------|---------|
| A | Server | Hostname (primary key) |
| B | Server Category | OS type (Windows/Linux) |
| C | Scope | In Scope / Out of Scope |
| D | Associated Apps | Application grouping |
| E | Associated Envs | Environment (Prod/Dev/etc.) |
| G | Current Cores | CPU core count |
| H | Current CPU Usage (%) | Avg CPU utilization |
| I | Current RAM (MB) | Total memory |
| J | Current Memory Usage (%) | Avg memory utilization |
| K | Storage (GB) | Total storage |

#### Servers Sheet — IGNORE these (agent derives its own)

| Column | Header | Reason |
|--------|--------|--------|
| F | Migration Strategy | Agent recommends via 6R |
| L | Target Azure Region | Agent prompts user |
| M | Chosen SKU | Agent recommends via MCP Azure |
| N-T | Payment/Settings | Agent prompts user |
| U-AA | Cost columns | Agent calculates via MCP Pricing |

### Step 5: Read Disks Sheet

```
Tool: mcp_excel-mcp_range
Action: get-values
Sheet: Disks
Range: A6:Y6   (headers)
```

Then read data rows: `Range: A7:Y<last_row>`

#### Disks Sheet — Input Columns (USE these)

| Column | Header | Purpose |
|--------|--------|---------|
| A | Server | FK to Servers sheet |
| G | Disk Name | Disk identifier |
| H | Disk Size (GB) | Capacity |
| I | Disk Read (MBPS) | Throughput |
| J | Disk Write (MBPS) | Throughput |
| K | Disk Read (IOPS) | IOPS |
| L | Disk Write (IOPS) | IOPS |
| Q | Storage Target | Managed Disk or Blob |

### Step 6: Correlate Servers to Disks

Join Servers and Disks by matching column A ("Server") in both sheets.

### Step 6b-6e: Open & Read App-to-Server Export

Open the App-to-Server Export, read "App-to-Server List" sheet (headers at row 4, data from row 5):

| Column | Header | Purpose |
|--------|--------|---------|
| A | Server | Hostname (join key) |
| B | Assessment Scope | In/Out |
| C | Application Name | Application grouping |
| D | Environment | Prod / Dev / UAT |
| E | Treatment | 6R suggestion |
| H | Power Status | On / Off |
| I | Operating System | Full OS version |
| J | Data Center | Source location |
| K | SQL Detected | Yes / No |

Correlate by Application Name: Rightsizing "Associated Apps" (col D) == App-to-Server "Application Name" (col C)

### Step 7: Build Workload Groups

Group servers using "Associated Apps" column. Unclassified servers (null/empty/"N/A"/"Unknown") get grouped into "Unclassified" group.

### Step 8: Prompt for Spoke Segmentation

### Step 9: Close Session

## Single-File Mode (FR-028–FR-032)

### Sheet Scanning

Scan ALL sheets, score by matching column patterns. Select highest-scoring sheet.

### Fuzzy Column-Name Matching

| Canonical Field | Recognized Variations |
|----------------|----------------------|
| `server_name` | "Server", "Server Name", "Host Name", "Hostname", "Machine Name", "Computer Name" |
| `application_name` | "Application", "Application Name", "App", "Workload", "Associated Apps" |
| `os_version` | "Operating System", "OS", "OS Version" |
| `environment` | "Environment", "Env", "Associated Envs" |
| `cpu_cores` | "Cores", "CPU Cores", "vCPU", "Current Cores" |
| `cpu_utilization` | "CPU Usage", "CPU Usage (%)", "Current CPU Usage (%)" |
| `ram_mb` | "RAM", "RAM (MB)", "Memory", "Current RAM (MB)" |
| `ram_utilization` | "Memory Usage", "Memory Usage (%)", "Current Memory Usage (%)" |
| `storage_gb` | "Storage", "Storage (GB)", "Total Storage", "Disk Size" |
| `disk_name` | "Disk Name", "disks type", "Volume" |
| `disk_iops` | "IOPS", "Disk IOPS" |
| `sql_detected` | "SQL Detected", "SQL Server" |
| `power_status` | "Power Status", "Power State" |
| `scope` | "Scope", "Assessment Scope" |

### Comma-Delimited Disk Parsing

When disk data is stored as comma-separated values in single cells:
1. Split by comma delimiter
2. Trim whitespace
3. Create one disk record per value
4. Maintain positional alignment across disk columns

Example:
```
Source: "S6, S10, S20" in disk type and "50, 100, 300" in disk size
Result: 3 disks → [{S6, 50GB}, {S10, 100GB}, {S20, 300GB}]
```

### Column Mapping Confirmation Report

Present mapping to user before extracting data:
```
## Column Mapping Report
| # | Source Header | → Mapped Field | Confidence |
|---|---|---|---|
| 1 | "Server" | server_name | 100% |
...
Proceed with data extraction? (yes/no)
```

## Error Handling

| Error | Action |
|-------|--------|
| IRM-protected file | Re-open with `show: true`, prompt for auth |
| Sheet not found | Try alternate names; if none, abort |
| Column mismatch | Report missing columns, attempt best-effort |
| Server name mismatch | Normalize: trim, case-insensitive, strip domain suffix |

## MCP Tools Used

- `mcp_excel-mcp_file` — Open/close Excel sessions
- `mcp_excel-mcp_worksheet` — List sheets
- `mcp_excel-mcp_range` — Read cell values and ranges
