---
mode: agent
description: "Generate an Azure cost estimate from an existing server inventory CSV."
---

# Generate Azure Cost Estimate

Automate the Azure Pricing Calculator using an existing server inventory CSV file.

## Prerequisites
- Server inventory CSV with columns: server, sku_name, os_type, ahub, region, storage_gb, disk_types
- Playwright MCP server configured

## Steps
1. Load and validate the CSV file
2. Group servers by SKU for batch entry
3. Open Azure Pricing Calculator via Playwright
4. Add Virtual Machines with correct SKU, OS, and payment model
5. Add Managed Disks based on disk type and capacity
6. Apply AHUB and Reserved Instance settings
7. Capture screenshot and shareable URL
8. Cross-validate totals against expected server count

## Output
- Azure Calculator shareable URL
- Screenshot of estimate
- Cost summary breakdown by SKU family
