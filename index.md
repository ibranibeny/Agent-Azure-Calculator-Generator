---
layout: home
title: Home
nav_order: 1
description: "VS Code custom agent for Azure infrastructure migration with hub-and-spoke network, VM right-sizing, and automated Azure Pricing Calculator estimates."
permalink: /
---

# Agent Azure Calculator Generator
{: .fs-9 }

A VS Code custom agent (`@BoM-Infra-calculator`) that automates **end-to-end Azure infrastructure migration assessments** — from Excel server inventory through VM right-sizing, hub-and-spoke network design, and Azure Pricing Calculator automation.
{: .fs-6 .fw-300 }

[Get Started]({{ site.baseurl }}{% link docs/installation.md %}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Skills]({{ site.baseurl }}{% link docs/skills.md %}){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What It Does

| Step | Action | Output |
|------|--------|--------|
| 1 | **Ingest server inventory** from Excel | Parsed server data |
| 2 | **Apply 6R migration strategy** | Rehost/Replatform/Refactor decisions |
| 3 | **Right-size VMs** | D/E/F-series SKU assignments |
| 4 | **Design hub-and-spoke network** | CIDR allocation, spoke segmentation |
| 5 | **Generate consolidated CSV** | All sizing decisions with rationale |
| 6 | **Validate output** against source | Mandatory pre-gate reconciliation |
| 7 | **Automate Azure Pricing Calculator** | Formal cost estimate via Playwright |
| 8 | **Produce assessment report** | Architecture diagrams + cost breakdown |

---

## Architecture at a Glance

| Component | Technology | Purpose |
|-----------|-----------|---------|
| 🤖 Agent Runtime | GitHub Copilot Chat | Orchestrates the 8-turn workflow |
| 📊 Excel Parsing | Excel MCP Server | COM automation for `.xlsx` ingestion |
| ☁️ Azure Pricing | Azure MCP Server | Live SKU availability & cost queries |
| 📚 Documentation | Microsoft Learn MCP | Architecture best-practice validation |
| 🌐 Calculator | Playwright MCP Server | Browser automation for formal estimates |
| 🐍 Scripts | Python + openpyxl | VM sizing logic & CSV enrichment |

---

## 8-Turn Agent Protocol

| Turn | Phase | Output |
|------|-------|--------|
| 1 | Excel Ingestion | Parsed server data, column mapping |
| 2 | Data Validation | Server count, scope filter, OS detection |
| 3 | Architecture Design | Hub-spoke topology, spoke segmentation |
| 4 | VM Right-Sizing | SKU assignments with rationale |
| 5 | User Confirmation | Buffer, AHUB, payment model preferences |
| 6 | CSV Generation | Consolidated server inventory CSV |
| 7 | Calculator Automation | Azure Pricing Calculator estimate |
| 8 | Final Report | Assessment document with all findings |

---

## Key Design Decisions

- **D/E/F-series only** — Never B-series (burstable) due to unpredictable migration performance
- **Hub-and-spoke topology** — Single hub with Azure Firewall; isolated spokes per workload
- **Data-driven sizing** — Utilization-based with 20% buffer (configurable)
- **Mandatory validation** — CSV reconciliation gate before Calculator automation
- **Zero manual Calculator entry** — Full Playwright automation for reproducible estimates

---

{: .note }
> This agent requires **Windows** for the Excel MCP Server (COM automation). Playwright MCP works cross-platform.

---

## Quick Start

In VS Code Copilot Chat:
```
@BoM-Infra-calculator Migrate my servers from C:\path\to\server-inventory.xlsx
```

Or with two Azure Migrate export files:
```
@BoM-Infra-calculator Migrate using:
- Rightsizing: C:\exports\Rightsizing-Export.xlsx
- App-to-Server: C:\exports\App-to-Server-Export.xlsx
```
