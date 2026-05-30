---
description: "Use when generating output files (Markdown assessment reports or CSV inventories) to ensure consistent metadata headers are included."
applyTo: "output/**"
---

# Output Metadata Headers

## Markdown Report Header

Every generated Markdown assessment report MUST begin with this metadata block:

```markdown
---
customer: "{customer_name}"
generated: "{ISO-8601 timestamp}"
agent: "BoM-Infra-calculator"
version: "1.0"
source_files:
  - "{filename1.xlsx}"
  - "{filename2.xlsx}"
target_region: "{azure_region}"
---
```

## CSV File Header Comment

CSV files include a comment header (lines starting with #) before the data header row:

```csv
# Customer: {customer_name}
# Generated: {ISO-8601 timestamp}
# Agent: BoM-Infra-calculator v1.0
# Source: {source_file_names}
# Region: {target_azure_region}
# Servers: {total_server_count}
# Disks: {total_disk_count}
server_name,application_name,environment,...
```

## Rules

1. **Always include metadata** — never generate output files without headers
2. **Timestamp format**: ISO-8601 with timezone (e.g., `2024-01-15T14:30:00Z`)
3. **Customer name**: Derived from input filename or user-provided at Turn 1
4. **Source files**: List all Excel files used as input
5. **Version**: Increment if agent behavior changes significantly
