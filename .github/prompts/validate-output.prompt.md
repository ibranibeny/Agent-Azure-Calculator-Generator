---
mode: agent
description: "Validate migration output (CSV/Calculator) against source Excel data."
---

# Validate Migration Output

Run accuracy validation to ensure the generated CSV and Azure Calculator estimate match the source Excel data.

## Validation Checks
1. **Row count** — Total servers in CSV matches source Excel (minus excluded)
2. **Server names** — Every in-scope server from Excel appears in CSV
3. **Disk entries** — Disk count and capacity match source
4. **SKU assignment** — VM family selection follows documented rules
5. **No duplicates** — Each server appears exactly once
6. **Exclusions documented** — All excluded servers listed with reasons

## Usage
Provide both the source Excel file and the generated CSV. The agent will perform a line-by-line reconciliation and report any discrepancies.

## Expected Output
- Accuracy percentage (target: 100%)
- List of any missing/mismatched servers
- Field-level discrepancy report
