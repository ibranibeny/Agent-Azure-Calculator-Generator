"""
Azure VM Right-Sizing Script
Reads server inventory from Excel (via openpyxl) and generates a sized CSV.
Customizable: region, buffer, AHUB, exclusion rules.

Usage:
  python scripts/vm_sizing.py --input <excel-file> --region <azure-region> --buffer 20
"""
import csv
import os
import re
import argparse

# --- Azure VM SKU catalog ---
D_SERIES = [
    ("Standard_D2as_v5", 2, 8),
    ("Standard_D4as_v5", 4, 16),
    ("Standard_D8as_v5", 8, 32),
    ("Standard_D16as_v5", 16, 64),
    ("Standard_D32as_v5", 32, 128),
    ("Standard_D48as_v5", 48, 192),
    ("Standard_D64as_v5", 64, 256),
    ("Standard_D96as_v5", 96, 384),
]

E_SERIES = [
    ("Standard_E2as_v5", 2, 16),
    ("Standard_E4as_v5", 4, 32),
    ("Standard_E8as_v5", 8, 64),
    ("Standard_E16as_v5", 16, 128),
    ("Standard_E20as_v5", 20, 160),
    ("Standard_E32as_v5", 32, 256),
    ("Standard_E48as_v5", 48, 384),
    ("Standard_E64as_v5", 64, 512),
    ("Standard_E96as_v5", 96, 672),
]

F_SERIES = [
    ("Standard_F2s_v2", 2, 4),
    ("Standard_F4s_v2", 4, 8),
    ("Standard_F8s_v2", 8, 16),
    ("Standard_F16s_v2", 16, 32),
    ("Standard_F32s_v2", 32, 64),
    ("Standard_F48s_v2", 48, 96),
    ("Standard_F64s_v2", 64, 128),
]


def select_sku(required_vcpus, required_ram_gb, family):
    """Find smallest SKU meeting requirements."""
    catalog = {"D": D_SERIES, "E": E_SERIES, "F": F_SERIES}[family]
    for sku_name, vcpus, ram in catalog:
        if vcpus >= required_vcpus and ram >= required_ram_gb:
            return sku_name, vcpus, ram
    # Fallback to largest in family
    return catalog[-1]


def determine_family(category, cpu_util, mem_util):
    """Select VM family based on server category and utilization profile."""
    if category == "SQL":
        return "E", "SQL server → memory-optimized"
    if mem_util > cpu_util * 2 and mem_util > 30:
        return "E", "Memory-heavy utilization profile"
    if cpu_util > mem_util * 2 and cpu_util > 30:
        return "F", "CPU-heavy utilization profile"
    return "D", "General-purpose (balanced)"


def is_excluded_os(os_str):
    """Check if Windows OS is below 2016 (excluded from migration)."""
    if not os_str:
        return False
    os_lower = os_str.lower()
    # Keep all Linux/FreeBSD/other non-Windows
    if any(x in os_lower for x in ['linux', 'centos', 'ubuntu', 'red hat', 'rhel', 'sles', 'suse', 'freebsd', 'other']):
        return False
    # Exclude Windows versions below 2016
    if 'windows server 2003' in os_lower:
        return True
    if 'windows server 2008' in os_lower:
        return True
    if 'windows server 2012' in os_lower:
        return True
    return False


def parse_disk_info(disk_types_str, disk_capacity_str):
    """Parse comma-delimited disk info."""
    disks = []
    if not disk_types_str or not disk_capacity_str:
        return disks
    types = [t.strip() for t in str(disk_types_str).split(',')]
    caps_raw = str(disk_capacity_str).split(',')
    caps = []
    for c in caps_raw:
        try:
            caps.append(float(c.strip()))
        except (ValueError, TypeError):
            caps.append(0)
    for i in range(max(len(types), len(caps))):
        t = types[i] if i < len(types) else "Unknown"
        c = caps[i] if i < len(caps) else 0
        disks.append((t, c))
    return disks


def map_disk_to_azure(disk_type, size_gb):
    """Map source disk to Azure Managed Disk type."""
    if 'premium ssd v2' in disk_type.lower():
        return "Premium SSD v2", disk_type
    if 'standardssd' in disk_type.lower():
        return "Standard SSD", disk_type
    if size_gb > 2048:
        return "Premium SSD", f"P50+ ({size_gb:.0f} GB)"
    elif size_gb > 512:
        return "Premium SSD", f"P30-P40 ({size_gb:.0f} GB)"
    elif size_gb > 128:
        return "Standard SSD", f"E15-E30 ({size_gb:.0f} GB)"
    else:
        return "Standard SSD", f"E6-E10 ({size_gb:.0f} GB)"


def size_servers(servers_data, buffer=0.20, region="southeastasia"):
    """
    Process server data and return included/excluded lists.
    
    servers_data: list of dicts with keys:
        server, disk_types, disk_capacity, os, category, scope, app, env,
        cores, cpu_pct, ram_mb, mem_pct, storage_gb
    """
    included = []
    excluded = []

    for s in servers_data:
        # Exclusion checks
        if s.get('scope', '').lower() != 'in scope':
            excluded.append({**s, 'reason': 'Out of Scope'})
            continue
        if is_excluded_os(s.get('os', '')):
            excluded.append({**s, 'reason': f"Unsupported OS: {s['os']}"})
            continue

        # Right-sizing calculation
        ram_gb = float(s.get('ram_mb', 0)) / 1024.0
        cpu_util = min(float(s.get('cpu_pct', 0)), 100.0)
        mem_util = min(float(s.get('mem_pct', 0)), 100.0)
        cores = int(s.get('cores', 2))

        required_vcpus = max(2, round((cpu_util / 100.0) * cores * (1 + buffer)))
        required_ram_gb = max(2, (mem_util / 100.0) * ram_gb * (1 + buffer))

        # Determine family
        family, rationale = determine_family(s.get('category', ''), cpu_util, mem_util)
        sku_name, sku_vcpus, sku_ram = select_sku(required_vcpus, required_ram_gb, family)

        # Determine OS type
        os_ver = s.get('os', '')
        category = s.get('category', '')
        os_type = "Linux" if category == "Linux" or any(
            x in os_ver.lower() for x in ['linux', 'centos', 'ubuntu', 'red hat', 'rhel', 'sles', 'suse', 'freebsd', 'other']
        ) else "Windows"

        included.append({
            "server": s['server'],
            "os": os_ver,
            "category": category,
            "environment": s.get('env', 'Unknown'),
            "cores": cores,
            "cpu_util": s.get('cpu_pct', 0),
            "ram_mb": s.get('ram_mb', 0),
            "ram_gb": round(ram_gb, 2),
            "mem_util": s.get('mem_pct', 0),
            "storage_gb": s.get('storage_gb', 0),
            "disk_types": s.get('disk_types', ''),
            "disk_capacity": s.get('disk_capacity', ''),
            "required_vcpus": required_vcpus,
            "required_ram_gb": round(required_ram_gb, 2),
            "sku_family": family,
            "family_rationale": rationale,
            "sku_name": sku_name,
            "sku_vcpus": sku_vcpus,
            "sku_ram_gb": sku_ram,
            "os_type": os_type,
            "ahub": "Yes" if os_type == "Windows" else "N/A",
            "strategy": "Rehost",
            "region": region,
            "sizing_method": "right-sized",
        })

    return included, excluded


def write_output(included, excluded, output_dir, customer_name):
    """Write CSV output files."""
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{customer_name}-server-inventory.csv")

    fieldnames = [
        "server", "os", "category", "environment", "cores", "cpu_util",
        "ram_mb", "ram_gb", "mem_util", "storage_gb", "disk_types", "disk_capacity",
        "required_vcpus", "required_ram_gb", "sku_family", "family_rationale",
        "sku_name", "sku_vcpus", "sku_ram_gb", "os_type", "ahub", "strategy", "region", "sizing_method"
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(included)

    # Write excluded servers
    excluded_path = os.path.join(output_dir, f"{customer_name}-excluded-servers.csv")
    with open(excluded_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["server", "os", "category", "scope", "app", "env", "exclusion_reason"])
        for e in excluded:
            writer.writerow([e.get('server', ''), e.get('os', ''), e.get('category', ''),
                           e.get('scope', ''), e.get('app', ''), e.get('env', ''), e.get('reason', '')])

    print(f"✅ Generated: {csv_path}")
    print(f"   Included servers: {len(included)}")
    print(f"   Excluded servers: {len(excluded)}")
    print(f"✅ Excluded list: {excluded_path}")

    # Summary stats
    families = {}
    for s in included:
        families[s['sku_family']] = families.get(s['sku_family'], 0) + 1
    print(f"\n📊 SKU Family Distribution:")
    for fam, count in sorted(families.items()):
        print(f"   {fam}-series: {count} servers")

    return csv_path, excluded_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Azure VM Right-Sizing from server data")
    parser.add_argument("--region", default="southeastasia", help="Target Azure region")
    parser.add_argument("--buffer", type=float, default=20, help="Buffer percentage (default: 20)")
    parser.add_argument("--customer", default="Customer", help="Customer name for output files")
    parser.add_argument("--output", default="output/migration-plan", help="Output directory")
    args = parser.parse_args()

    print(f"VM Sizing Script - Region: {args.region}, Buffer: {args.buffer}%")
    print("Note: This script is typically invoked by the @BoM-Infra-calculator agent")
    print("      which reads server data from Excel via MCP tools.")
    print("      For standalone use, provide server data programmatically.")
