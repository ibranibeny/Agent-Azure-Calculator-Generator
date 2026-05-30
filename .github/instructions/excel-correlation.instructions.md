---
description: "Use when correlating Azure Rightsizing Export with App-to-Server Export, joining by server hostname, handling unmatched servers, or determining the master server list."
applyTo: "**"
---

# Two-File Excel Correlation Rules

## Join Method

The two Excel files are correlated by **server hostname**:

```
Rightsizing Export "Server" (col A) == App-to-Server Export "Server" (col A)
```

## Master List Rule

The **Rightsizing Export is the primary/master server list**. Every server in it MUST be assessed:

- Match found in App-to-Server → enrich with OS, environment, SQL status, power state
- No match in App-to-Server → flag as "OS version unknown", STILL include in sizing
- Server only in App-to-Server → note as "no sizing data available", exclude from VM right-sizing

## OS Type Inclusion

Include **ALL operating system types**: Windows Server, Linux (RHEL, Ubuntu, CentOS, SLES), Other/Unknown.

Do NOT filter out non-Windows servers.

## Unclassified Server Handling

Servers with blank or generic `applicationName` values → group into "Unclassified":

### Detection Patterns (case-insensitive)
- null / empty / whitespace-only
- "N/A", "NA", "n/a", "Unknown", "TBD"
- Single character (e.g., "-", ".", "x")
- Numeric-only values (e.g., "123", "0")

### Handling
1. Group into single "Unclassified" workload group
2. Present separately from named workload groups
3. Prompt user to assign, create new group, or keep as-is

## Deduplication Rules

A server may appear multiple times in App-to-Server Export:

- **For OS extraction**: Use first non-empty OS value
- **For application mapping**: Preserve ALL rows (multi-app)
- **For SQL detection**: If ANY row shows `sqlDetected = Yes`, treat as SQL-hosting

## Column Reference

### Rightsizing Export (Servers sheet, headers at row 6)

| Column | Header | Purpose |
|--------|--------|---------|
| A | Server | Hostname (primary key) |
| B | Server Category | OS type (Windows/Linux) |
| C | Scope | In/Out of scope |
| D | Associated Apps | Application grouping |
| E | Associated Envs | Environment |
| G | Current Cores | CPU sizing input |
| H | Current CPU Usage (%) | Utilization |
| I | Current RAM (MB) | Memory sizing input |
| J | Current Memory Usage (%) | Utilization |
| K | Storage (GB) | Total storage |

### App-to-Server Export (headers at row 4)

| Column | Header | Purpose |
|--------|--------|---------|
| A | Server | Hostname (for cross-ref) |
| B | Assessment Scope | In/Out of scope |
| C | Application Name | Application grouping |
| D | Environment | Prod/Dev/UAT |
| E | Treatment | 6R suggestion |
| H | Power Status | On/Off |
| I | Operating System | Full OS version string |
| J | Data Center | Source location |
| K | SQL Detected | Yes/No |

## Validation

After correlation, verify:
1. Every server in Rightsizing has a workload group assignment
2. No server is double-counted (unless multi-app)
3. Total server count matches Rightsizing Export row count (minus out-of-scope)
