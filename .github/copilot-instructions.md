# Azure Calculator Generator — Copilot Instructions

## Project Overview

This repository provides a **VS Code custom agent** (`@BoM-Infra-calculator`) that automates Azure infrastructure migration assessments. It ingests server inventory Excel files, performs VM right-sizing, designs hub-and-spoke network architecture, generates cost estimates, and automates the Azure Pricing Calculator.

## Available Agent

- `@BoM-Infra-calculator` — Azure infrastructure migration agent with hub-and-spoke design, 6R strategy assessment, Excel data ingestion, Azure pricing, and Calculator automation via Playwright.

## Key Principles

1. **Hub-and-Spoke Architecture** — All migrations use hub-spoke network topology
2. **6R Migration Framework** — Rehost, Replatform, Refactor, Rearchitect, Rebuild, Replace
3. **Data-Driven Decisions** — All sizing from Excel source data, not assumptions
4. **Live Azure Pricing** — Real-time pricing via Azure MCP tools
5. **Security by Default** — No public IPs, NSGs everywhere, Firewall for all traffic
6. **NO B-SERIES** — Never recommend burstable VMs for any workload

## Skills Available

| Skill | Purpose |
|-------|---------|
| `excel-data-ingestion` | Parse Excel files (two-file and single-file modes) |
| `excel-to-csv-analysis` | Generate consolidated CSV from Excel data |
| `azure-calculator-automation` | Automate Azure Pricing Calculator via Playwright |
| `calculator-from-csv` | Generate Calculator estimate from CSV file |
| `azure-cost-availability` | Check pricing and SKU availability per region |
| `accuracy-validation` | Validate CSV/Calculator output vs source Excel |
| `csv-source-reconciliation` | Mandatory pre-gate before Calculator automation |
| `best-practice-architecture` | Validate against Microsoft Learn best practices |

## Instructions Available

| Instruction | Scope |
|-------------|-------|
| `vm-sizing` | VM SKU selection logic and family priority |
| `hub-spoke-design` | Network architecture and CIDR allocation |
| `excel-correlation` | Two-file join rules by server hostname |
| `diagram-generation` | Python Diagrams library for architecture diagrams |
| `output-metadata` | Consistent metadata headers on all output files |
