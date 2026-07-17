#!/usr/bin/env python3
"""
ptai-fix: Wrapper untuk ptai dengan LLM disabled, timeout fixed.
Guna: python3 ptai-fix.py <target>
"""

import os, sys, subprocess, json, time

TARGET = sys.argv[1] if len(sys.argv) > 1 else "https://my.myfirst.tech/"

# Env untuk ptai — LLM disabled, model irrelevant
env = os.environ.copy()
env.update({
    "OPENAI_API_KEY": "sk-wUY8v4NqoqedTXpY680bPqChrybNBniiihKp4BKp4sTi8IFlD19sGcO64F5YGMbI",
    "OPENAI_BASE_URL": "https://opencode.ai/zen/go/v1",
    "PENTEST_AI_AUP_ACCEPTED": "1",
    "PENTEST_AI_LLM_PROVIDER": "skip",  # No LLM
    "PENTEST_AI_MODEL": "",
})

PHASES = [
    ("[PHASE 1] RECON — whatweb, httpx, nmap, wafw00f", "recon"),
    ("[PHASE 2] CONTENT DISCOVERY — gobuster, ffuf, dirsearch", "content_discovery"),
    ("[PHASE 3] VULN SCAN — nuclei, nikto", "vulnerability"),
    ("[PHASE 4] DEEP SCAN — sqlmap, dalfox, wpscan (if applicable)", "exploitation"),
]

def run_phase(name, phase_id):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    
    cmd = [
        "ptai", "start",
        "--no-llm",
        "--intensity", "normal" if phase_id != "exploitation" else "aggressive",
        TARGET
    ]
    
    # For content_discovery, reduce dirsearch timeout
    my_env = env.copy()
    if phase_id == "content_discovery":
        my_env["PENTEST_AI_DIRSEARCH_TIMEOUT"] = "60"
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=my_env)
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr[-500:]}")
    
    # Get the latest engagement ID
    list_proc = subprocess.run(["ptai", "list"], capture_output=True, text=True, env=env)
    # Extract ID from first line of output
    for line in list_proc.stdout.split("\n"):
        if "│" in line and "https" in line:
            parts = [p.strip() for p in line.split("│")]
            if len(parts) >= 2:
                print(f"  → Engagement ID: {parts[1]}")
                return parts[1]
    return None

def show_findings(eid):
    if not eid:
        return
    proc = subprocess.run(["ptai", "findings", eid], capture_output=True, text=True, env=env)
    print(f"\n📊 FINDINGS for {eid}:")
    lines = proc.stdout.split("\n")
    critical = [l for l in lines if "CRITICAL" in l]
    high = [l for l in lines if "HIGH" in l and "CRITICAL" not in l]
    medium = [l for l in lines if "MEDIUM" in l]
    low = [l for l in lines if "LOW" in l]
    info = [l for l in lines if "INFO" in l]
    
    print(f"  🔴 CRITICAL: {len(critical)}")
    for c in critical[:5]: print(f"     {c}")
    print(f"  🟠 HIGH: {len(high)}")
    print(f"  🟡 MEDIUM: {len(medium)}")
    print(f"  🔵 LOW: {len(low)}")
    print(f"  ⚪ INFO: {len(info)}")

# Run phases
print(f"\n🎯 TARGET: {TARGET}")
print(f"🔧 LLM: DISABLED (offline tools only)")

for phase_name, phase_id in PHASES:
    eid = run_phase(phase_name, phase_id)
    if eid:
        show_findings(eid)
    # Brief pause between phases
    time.sleep(2)

print(f"\n{'='*60}")
print("✅ SCAN COMPLETE!")
print(f"{'='*60}")
