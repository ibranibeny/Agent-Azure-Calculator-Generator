---
mode: agent
description: "Run a full Azure migration assessment from an Excel server inventory file."
---

# Migrate Servers to Azure

Perform a complete Azure infrastructure migration assessment using the @BoM-Infra-calculator agent workflow.

## Input Required
- Excel file containing server inventory (single-file or two-file format)
- Target Azure region
- Buffer percentage for right-sizing (default: 20%)

## Workflow
1. Ingest Excel data and validate columns
2. Apply 6R migration strategy
3. Design hub-and-spoke network architecture
4. Right-size VMs (D/E/F series, NEVER B-series)
5. Generate server inventory CSV
6. Validate CSV against source data
7. Automate Azure Pricing Calculator
8. Produce final assessment report

## Usage
Provide your Excel file path when prompted. The agent will guide you through each step.
