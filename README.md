# Agent-Azure-Calculator-Generator

A VS Code custom agent (`@BoM-Infra-calculator`) that automates end-to-end Azure infrastructure migration assessments — from Excel server inventory ingestion through VM right-sizing, hub-and-spoke network design, cost estimation, and Azure Pricing Calculator automation.

## What It Does

1. **Ingests server inventory** from Excel files (single consolidated file or two-file Azure Migrate export format)
2. **Applies 6R migration strategy** (Rehost, Replatform, Refactor, Rearchitect, Rebuild, Replace)
3. **Right-sizes VMs** using D-series (general), E-series (memory/SQL), F-series (compute) — **never B-series**
4. **Designs hub-and-spoke network** with CIDR allocation, spoke segmentation, and infrastructure server placement
5. **Generates consolidated CSV** with all sizing decisions and rationale
6. **Validates output** against source data (mandatory pre-gate)
7. **Automates Azure Pricing Calculator** via Playwright for formal cost estimates
8. **Produces assessment report** with architecture diagrams and cost breakdown

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
| openpyxl | Excel parsing (`pip install openpyxl`) |
| Graphviz | Architecture diagram rendering |

### MCP Server Configuration

Add these to your VS Code `settings.json` or `.vscode/mcp.json`:

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

Refer to each MCP server's documentation for installation commands.

## Installation

1. Clone this repository into your workspace:
   ```bash
   git clone https://github.com/your-org/Agent-Azure-Calculator-Generator.git
   ```

2. Open in VS Code:
   ```bash
   code Agent-Azure-Calculator-Generator
   ```

3. Install Python dependencies:
   ```bash
   pip install openpyxl diagrams
   ```

4. Ensure MCP servers are configured (see Prerequisites)

5. The `@BoM-Infra-calculator` agent becomes available in GitHub Copilot Chat

## Usage

### Quick Start

In VS Code Copilot Chat:
```
@BoM-Infra-calculator Migrate my servers from C:\path\to\server-inventory.xlsx
```

### With Two Files (Azure Migrate Exports)
```
@BoM-Infra-calculator Migrate using:
- Rightsizing: C:\exports\Rightsizing-Export.xlsx
- App-to-Server: C:\exports\App-to-Server-Export.xlsx
```

### Custom Options
```
@BoM-Infra-calculator Migrate C:\data\servers.xlsx to westus2 with 30% buffer
```

## 8-Turn Agent Protocol

The agent follows a structured 8-turn workflow:

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

## Directory Structure

```
.github/
├── agents/
│   └── BoM-Infra-calculator.agent.md    # Agent definition
├── instructions/
│   ├── vm-sizing.instructions.md         # VM SKU selection rules
│   ├── hub-spoke-design.instructions.md  # Network architecture
│   ├── excel-correlation.instructions.md # Two-file join logic
│   ├── diagram-generation.instructions.md# Python Diagrams conventions
│   └── output-metadata.instructions.md  # Output file headers
├── skills/
│   ├── excel-data-ingestion/SKILL.md     # Excel parsing procedures
│   ├── excel-to-csv-analysis/SKILL.md    # CSV generation
│   ├── azure-calculator-automation/SKILL.md # Calculator via Playwright
│   ├── calculator-from-csv/SKILL.md      # Calculator from CSV
│   ├── azure-cost-availability/SKILL.md  # Pricing/SKU checks
│   ├── accuracy-validation/SKILL.md      # Output validation
│   ├── csv-source-reconciliation/SKILL.md# Mandatory pre-gate
│   └── best-practice-architecture/SKILL.md # Architecture validation
├── prompts/
│   ├── migrate-servers.prompt.md         # Full migration workflow
│   ├── generate-cost-estimate.prompt.md  # Calculator automation
│   └── validate-output.prompt.md         # Output validation
└── copilot-instructions.md               # Project-level instructions
scripts/
├── vm_sizing.py                          # VM right-sizing logic
└── enrich_csv.py                         # CSV enrichment from Excel
samples/
└── excel-format-guide.md                 # Excel input format documentation
output/                                   # Generated outputs (gitignored)
├── migration-plan/                       # CSV and assessment reports
├── architecture/                         # Diagrams and scripts
└── cost-estimates/                       # Calculator screenshots/URLs
```

## Excel Input Format

### Single File (Recommended for New Projects)

A single `.xlsx` with 20 columns. Key columns:

| Column | Purpose |
|--------|---------|
| Server | Hostname (primary key) |
| Server Category | Windows / Linux / SQL |
| Scope | In Scope / Out of Scope |
| Current Cores | Allocated vCPUs |
| Current CPU Usage (%) | Average utilization |
| Current RAM (MB) | Allocated memory |
| Current Memory Usage (%) | Memory utilization |
| Storage (GB) | Total storage |
| disks type | Comma-separated disk types (S10, S20, etc.) |
| disk capacity (GB) | Comma-separated disk sizes |

See [samples/excel-format-guide.md](samples/excel-format-guide.md) for complete column reference.

### Two Files (Azure Migrate Exports)

- **Rightsizing Export** — Server specs, utilization, disk IOPS
- **App-to-Server Export** — OS version, SQL detection, environment

Files are correlated by server hostname.

## VM Sizing Rules

| Priority | Signal | VM Family |
|----------|--------|-----------|
| 1 | SQL Server detected | E-series (memory-optimized) |
| 2 | Memory-heavy utilization | E-series |
| 3 | CPU-heavy utilization | F-series (compute-optimized) |
| 4 | Default/balanced | D-series (general-purpose) |

- **Buffer**: 20% added to utilization-based sizing (configurable)
- **Minimum**: 2 vCPUs for all VMs
- **NEVER**: B-series (burstable) — unpredictable performance during migration
- **Excluded**: Windows Server < 2016 (2003, 2008, 2012)

## Network Architecture

Hub-and-spoke topology with:
- **Hub VNet** (10.0.0.0/16): Azure Firewall, VPN Gateway, SharedServices subnet
- **Spoke VNets** (10.x.0.0/16): One per workload group with web/app/data subnets
- **Peering**: All spokes peer to hub; inter-spoke traffic routes through firewall
- **Infrastructure servers**: Detected and placed in hub SharedServices subnet

## Customization

### Adding New VM Families

Edit `.github/instructions/vm-sizing.instructions.md` to add new family selection rules.

### Changing Network Design

Edit `.github/instructions/hub-spoke-design.instructions.md` for CIDR ranges, subnet allocation, or spoke segmentation options.

### Adding Skills

Create a new directory under `.github/skills/<skill-name>/SKILL.md` with procedural instructions the agent should follow.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Excel MCP can't open file | Close file in Excel desktop app (COM needs exclusive access) |
| IRM-protected Excel | Use `show: true` parameter in Excel MCP file open |
| Calculator automation fails | Ensure Playwright MCP is connected and browser is available |
| Zero utilization data | Agent falls back to allocated capacity (documented in output) |
| Missing OS column | Agent uses fuzzy column matching; check header spelling |

## License

MIT
