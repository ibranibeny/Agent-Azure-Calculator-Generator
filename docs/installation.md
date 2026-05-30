---
layout: default
title: Installation
nav_order: 2
description: "How to install the Agent Azure Calculator Generator into your workspace."
permalink: /installation/
---

# Installation
{: .fs-8 }

Two options to get started — scaffold into an existing project or clone standalone.
{: .fs-5 .fw-300 }

---

## Option A: Install into an Existing Project (Recommended)

Use `npx degit` to copy only the agent files into your current workspace — no git history, no conflicts with your existing files:

```bash
npx degit ibranibeny/Agent-Azure-Calculator-Generator/.github .github --force
npx degit ibranibeny/Agent-Azure-Calculator-Generator/scripts scripts
npx degit ibranibeny/Agent-Azure-Calculator-Generator/samples samples
```

This installs:
- `.github/agents/` — Agent definition
- `.github/skills/` — 8 procedural skill files
- `.github/instructions/` — VM sizing, network, and Excel rules
- `.github/prompts/` — Reusable prompt templates
- `scripts/` — Python sizing and enrichment scripts
- `samples/` — Example Excel input and format guide

{: .tip }
> `npx degit` downloads a folder from GitHub without cloning the entire repo. It requires Node.js 14+.

---

## Option B: Clone as Standalone Workspace

```bash
git clone https://github.com/ibranibeny/Agent-Azure-Calculator-Generator.git
cd Agent-Azure-Calculator-Generator
code .
```

---

## Post-Installation Setup

### 1. Install Python Dependencies

```bash
pip install openpyxl diagrams
```

### 2. Configure MCP Servers

Add to your VS Code `settings.json` or `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "excel-mcp": { "command": "..." },
      "azure": { "command": "..." },
      "microsoft-lea": { "command": "..." },
      "microsoft_pla": { "command": "..." }
    }
  }
}
```

Refer to each MCP server's documentation for specific installation commands.

### 3. Verify Agent Availability

Open VS Code Copilot Chat and type:
```
@BoM-Infra-calculator
```

If the agent appears in autocomplete, installation is complete.

---

## Prerequisites

| Requirement | Purpose |
|-------------|---------|
| VS Code (latest) | Host editor with GitHub Copilot |
| GitHub Copilot Chat | Agent runtime |
| Excel MCP Server | Read Excel files via COM automation (Windows) |
| Azure MCP Server | Pricing queries, SKU availability, region checks |
| Microsoft Learn MCP | Documentation validation |
| Playwright MCP Server | Azure Calculator browser automation |
| Python 3.8+ | Scripts and diagram generation |
| Node.js 14+ | For `npx degit` installation method |
| Graphviz | Architecture diagram rendering |

{: .important }
> The Excel MCP Server requires **Windows** (COM automation). All other components work cross-platform.

---

## Directory Structure

```
.github/
├── agents/
│   └── BoM-Infra-calculator.agent.md
├── instructions/
│   ├── vm-sizing.instructions.md
│   ├── hub-spoke-design.instructions.md
│   ├── excel-correlation.instructions.md
│   ├── diagram-generation.instructions.md
│   └── output-metadata.instructions.md
├── skills/
│   ├── excel-data-ingestion/SKILL.md
│   ├── excel-to-csv-analysis/SKILL.md
│   ├── azure-calculator-automation/SKILL.md
│   ├── calculator-from-csv/SKILL.md
│   ├── azure-cost-availability/SKILL.md
│   ├── accuracy-validation/SKILL.md
│   ├── csv-source-reconciliation/SKILL.md
│   └── best-practice-architecture/SKILL.md
├── prompts/
│   ├── migrate-servers.prompt.md
│   ├── generate-cost-estimate.prompt.md
│   └── validate-output.prompt.md
└── copilot-instructions.md
scripts/
├── vm_sizing.py
└── enrich_csv.py
samples/
├── server-inventory.xlsx
└── excel-format-guide.md
```
