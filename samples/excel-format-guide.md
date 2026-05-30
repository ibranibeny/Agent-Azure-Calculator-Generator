# Excel File Format — Sample Documentation

This document describes the expected Excel input formats for the `@BoM-Infra-calculator` agent.

## Option 1: Single Consolidated File

A single Excel file with all server data in one sheet.

### Sheet Structure

| Row | Content |
|-----|---------|
| 1 | DROP DOWN markers (columns N-T only) — used for Excel data validation, ignored by agent |
| 2 | **Column Headers** (20 columns) |
| 3+ | Server data rows |

### Column Headers (Row 2)

| Col | Header | Description | Example |
|-----|--------|-------------|---------|
| A | Server | Hostname (primary key) | `SL-INBATCH01` |
| B | disks type | Comma-separated disk types | `S10, S20` |
| C | disk capacity (GB) | Comma-separated capacities | `100, 300` |
| D | Operating System | Full OS version string | `Windows Server 2016 ServerStandard` |
| E | Server Category | Windows / Linux / SQL | `Windows` |
| F | Scope | In Scope / Out of Scope | `In Scope` |
| G | Associated Apps | Application name or group | `Finance-App` |
| H | Associated Envs | Environment | `Prod` |
| I | Migration Strategy | 6R strategy (reference) | `Rehost` |
| J | Current Cores | Allocated CPU cores | `8` |
| K | Current CPU Usage (%) | Average CPU utilization | `14.01` |
| L | Current RAM (MB) | Allocated memory in MB | `16384` |
| M | Current Memory Usage (%) | Average memory utilization | `31.84` |
| N | Storage (GB) | Total storage capacity | `200` |
| O | Target Azure Region | Azure region | `southeastasia` |
| P | Chosen SKU | Pre-selected SKU (optional) | _(blank = auto-size)_ |
| Q | Chosen Payment Model | PAYG / RI-1yr / RI-3yr | `RI-3yr` |
| R | Hybrid Benefit Setting | Yes / No | `Yes` |
| S | SQL Hybrid Benefit Setting | Yes / No / N/A | `N/A` |
| T | Dev/Test Setting | Yes / No | `No` |

### Important Notes

- **Row 1** may contain DROP DOWN markers in columns N-T — the agent skips this row
- **Headers are in Row 2** — the agent uses fuzzy matching to identify columns
- All data starts at **Row 3**
- Disk types and capacities are comma-delimited within a single cell
- Server Category "SQL" triggers E-series (memory-optimized) VM selection
- "Out of Scope" servers are excluded from sizing but documented

## Option 2: Two-File Format (Azure Migrate Exports)

### File 1: Azure Rightsizing Export

Contains server specs and utilization data.

**Servers Sheet** (headers at row 6):
| Col | Header | Purpose |
|-----|--------|---------|
| A | Server | Hostname (primary key) |
| B | Server Category | OS type |
| C | Scope | In/Out of scope |
| D | Associated Apps | Application grouping |
| E | Associated Envs | Environment |
| G | Current Cores | CPU cores |
| H | Current CPU Usage (%) | CPU utilization |
| I | Current RAM (MB) | Memory |
| J | Current Memory Usage (%) | Memory utilization |
| K | Storage (GB) | Total storage |

**Disks Sheet** (headers at row 6):
| Col | Header | Purpose |
|-----|--------|---------|
| A | Server | Hostname (join key) |
| G | Disk Name | Individual disk identifier |
| H | Disk Size GB | Disk capacity |
| K | Disk Read IOPS | Read performance |
| L | Disk Write IOPS | Write performance |

### File 2: App-to-Server Export

Contains OS version, environment, and SQL detection.

**App-to-Server List Sheet** (headers at row 4):
| Col | Header | Purpose |
|-----|--------|---------|
| A | Server | Hostname (join key) |
| C | Application Name | App grouping |
| D | Environment | Prod/Dev/UAT |
| H | Power Status | On/Off |
| I | Operating System | Full OS version |
| J | Data Center | Source location |
| K | SQL Detected | Yes/No |

### Correlation Rule

Files are joined by **server hostname**: `Rightsizing.Server == App-to-Server.Server`

The Rightsizing Export is the **master server list** — every server in it is assessed.

## Exclusion Rules

Servers are excluded from sizing (but documented) when:
- `Scope = "Out of Scope"`
- Windows OS version < 2016 (Server 2003, 2008, 2012)

## Sample Data

```csv
Server,disks type,disk capacity (GB),Operating System,Server Category,Scope,Associated Apps,Associated Envs,Migration Strategy,Current Cores,Current CPU Usage (%),Current RAM (MB),Current Memory Usage (%),Storage (GB),Target Azure Region
SL-INBATCH01,"S10, S10","100, 100",Windows Server 2016 ServerStandard,Windows,In Scope,BatchApp,Prod,Rehost,8,14.01,16384,31.84,200,southeastasia
SEG-DEVDLTAPP01_NEW,"S20, S40","300, 1200",Red Hat Enterprise Linux 7,Linux,In Scope,DLT-App,Prod,Rehost,16,30.98,131072,13.17,1500,southeastasia
SEG-FIN02,"S20, S15","400, 200",Windows Server 2019 ServerStandard,SQL,In Scope,Finance,Prod,Rehost,8,9.27,65536,12.64,600,southeastasia
```
