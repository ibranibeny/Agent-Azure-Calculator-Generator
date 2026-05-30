---
name: azure-calculator-automation
description: "Automate Azure Pricing Calculator via Playwright MCP to generate formal cost estimates. Use when: creating Azure Calculator estimates, automating pricing calculator, generating shareable cost URLs, taking calculator screenshots for proposals."
argument-hint: "Provide the VM sizing table and disk mapping results from the migration assessment"
---

# Azure Pricing Calculator Automation

## When to Use

- Generating a formal Azure Pricing Calculator estimate after VM right-sizing
- Automating the addition of VMs and managed disks to the calculator
- Producing a shareable URL or screenshot for customer proposals
- Creating a visual cost summary beyond the API-based pricing table

## Prerequisites

- Playwright MCP (`microsoft_pla`) must be available
- VM sizing table (from Turn 6 of the agent workflow) with: SKU, region, OS, pricing tier
- Disk mapping table with: disk type, size, count per server
- Target Azure region (from Turn 2)
- AHUB eligibility (from Turn 6/7)

## Procedure

### Step 1: Navigate to Azure Pricing Calculator

```
Tool: mcp_microsoft_pla_browser_navigate
URL: https://azure.microsoft.com/en-us/pricing/calculator/
```

Wait for page load. Take initial snapshot to confirm calculator is ready:
```
Tool: mcp_microsoft_pla_browser_snapshot
```

### Step 2: Add Virtual Machines (Per-Server, NOT Grouped)

For each individual server in the sizing table (one entry per server name, quantity always = 1):

1. Search for "Virtual Machines" in the calculator search bar
2. Configure the VM entry for THIS specific server:
   - **Name/Description**: The server hostname (e.g., "SQLPROD01") — for traceability
   - **Region**: Select the target region (from Turn 2)
   - **Operating System**: Windows or Linux (from this server's OS data)
   - **Type**: Select VM series (e.g., D-series, E-series) based on this server's vm_family
   - **Tier**: Standard
   - **Instance**: Select exact SKU size from this server's recommended_sku (e.g., D4s_v5)
   - **Quantity**: **1** (always 1 — each server is its own line item)
   - **Pricing Option**: 
     - Production servers → 1-year or 3-year Reserved Instance
     - Dev/Test servers → Pay-as-you-go
   - **Azure Hybrid Benefit**: Enable if user confirmed AHUB eligibility

3. Use form-filling tools:
   ```
   Tool: mcp_microsoft_pla_browser_select_option
   Tool: mcp_microsoft_pla_browser_fill_form
   Tool: mcp_microsoft_pla_browser_click
   ```

4. **Repeat for EVERY server** — do NOT group multiple servers into one entry with quantity > 1.

### Step 3: Add Managed Disks (Per-Disk, NOT Grouped)

For each disk entry associated with each server:

1. Add "Managed Disks" product to the calculator
2. Configure:
   - **Name/Description**: "{server_name} - {disk_name}" (e.g., "SQLPROD01 - Data_Disk_1")
   - **Region**: Same target region
   - **Type**: Premium SSD / Standard SSD / Standard HDD / Ultra Disk
   - **Size**: Disk tier (P30, E30, S30, etc.)
   - **Quantity**: **1** (always 1 — each disk is its own line item)
   - **Redundancy**: LRS (default for migration)

### Step 4: Add Networking Components

Add hub-spoke networking costs:
1. **Azure Firewall** — Standard tier, 1 instance
2. **VPN Gateway** or **ExpressRoute** — based on connectivity choice
3. **Virtual Network Peering** — based on spoke count
4. **Azure Bastion** — 1 instance for management access

### Step 5: Capture Results

1. Scroll to the total estimate section
2. Take screenshot:
   ```
   Tool: mcp_microsoft_pla_browser_take_screenshot
   ```
3. Save screenshot to `output/cost-estimates/calculator-screenshot.png`
4. Extract total monthly cost from page
5. Copy the shareable estimate URL (if available)

### Step 6: Close Browser

```
Tool: mcp_microsoft_pla_browser_close
```

## Output

- `output/cost-estimates/calculator-screenshot.png` — Visual screenshot
- Azure Calculator shareable URL (if available)
- Total monthly estimate extracted from the calculator
- Comparison: Calculator total vs. API-based pricing total

## Error Handling / Fallback

| Error | Action |
|-------|--------|
| Playwright MCP unavailable | Skip entirely; report pricing from API only |
| Page load timeout | Retry once; if fails, skip with note |
| Element not found (UI changed) | Log selector that failed; skip calculator |
| Region not available in dropdown | Use closest available region; note discrepancy |
| Too many VMs (calculator limit) | Add first 50 servers individually; note remainder |
| Authentication wall | Skip; note "Calculator requires sign-in" |

**Fallback**: Log failure reason, skip calculator, report pricing from MCP API results only.

## MCP Tools Used

- `mcp_microsoft_pla_browser_navigate` — Open calculator URL
- `mcp_microsoft_pla_browser_snapshot` — Read page state / DOM
- `mcp_microsoft_pla_browser_click` — Click buttons and product cards
- `mcp_microsoft_pla_browser_select_option` — Select dropdowns (region, OS, tier)
- `mcp_microsoft_pla_browser_fill_form` — Fill quantity and configuration fields
- `mcp_microsoft_pla_browser_take_screenshot` — Capture visual estimate
- `mcp_microsoft_pla_browser_close` — Clean up browser session
