#!/usr/bin/env python3
"""
RakyatHub Topic Rotation — picks the next topic in round-robin sequence.
Output is consumed by the master rotation cron agent.

State file: ~/AppData/Local/hermes/topic_rotation_state.json
"""
import json, os, sys, datetime

STATE_FILE = os.path.expanduser("~/AppData/Local/hermes/topic_rotation_state.json")

TOPICS = [
    {
        "id": "kesihatan",
        "title": "Kesihatan & Perubatan",
        "description": "Insurance, medical card, hospital costs, health tips, mental health",
        "focus_keywords": "insurans kesihatan, kos perubatan Malaysia, medical card, kemurungan"
    },
    {
        "id": "pendidikan",
        "title": "Pendidikan",
        "description": "UPU, biasiswa, SSPN, student tips, university prep, study loans",
        "focus_keywords": "UPU 2026, biasiswa Malaysia, SSPN, tips student universiti"
    },
    {
        "id": "hidup-sewa",
        "title": "Hidup Sewa",
        "description": "Renting tips, tenancy agreement, tenant rights, roommates, deposit disputes",
        "focus_keywords": "sewa rumah Malaysia, tenancy agreement, hak penyewa, bilik sewa"
    },
    {
        "id": "hak-pengguna",
        "title": "Hak Pengguna",
        "description": "Consumer rights, product returns, warranty, tribunal tuntutan, scam reports",
        "focus_keywords": "hak pengguna Malaysia, tribunal tuntutan, refund, warranty"
    },
    {
        "id": "insurans",
        "title": "Insurans",
        "description": "Insurance guides: life, medical, motor, travel, critical illness, takaful",
        "focus_keywords": "insurans hayat, medical card, takaful, insurans kereta"
    },
    {
        "id": "pandu-jalan-raya",
        "title": "Pandu Jalan Raya",
        "description": "Road tax, driving license, JPJ, saman, AES, car maintenance, first car",
        "focus_keywords": "cukai jalan, lesen memandu, saman JPJ, kereta pertama"
    },
    {
        "id": "gaya-hidup-bajet",
        "title": "Gaya Hidup Bajet",
        "description": "Budget lifestyle, grocery tips, save money, minimalis, cheap eats KL",
        "focus_keywords": "jimat duit, grocery murah, budget lifestyle, minimalis"
    },
    {
        "id": "teknologi-rakyat",
        "title": "Teknologi Rakyat",
        "description": "Tech gadgets, apps, AI tools, digital security, phone plans, internet",
        "focus_keywords": "teknologi Malaysia, AI tools, keselamatan digital, apps kewangan"
    },
    {
        "id": "kerja-bisnes-kecil",
        "title": "Kerja & Bisnes Kecil",
        "description": "Small business, dropship, reseller, side income, online business",
        "focus_keywords": "bisnes kecil Malaysia, dropship, reseller, pendapatan sampingan"
    },
    {
        "id": "bantuan-kerajaan",
        "title": "Bantuan Kerajaan",
        "description": "STR, SARA, eBelia, Sumbangan Asas, BPR, government aid guides",
        "focus_keywords": "STR 2026, SARA, eBelia, bantuan kerajaan, sara hidup"
    },
    {
        "id": "darurat-bencana",
        "title": "Darurat & Bencana",
        "description": "Flood prep, emergency kit, evacuation, fire safety, first aid, disaster aid",
        "focus_keywords": "banjir Malaysia, peti kecemasan, evakuasi, bomba, first aid"
    },
    {
        "id": "side-hustle",
        "title": "Side Hustle",
        "description": "Part-time jobs, gig economy, p-hailing, UGC content, freelancer tips",
        "focus_keywords": "side hustle Malaysia, p-hailing, freelancer, gig economy"
    },
    {
        "id": "daily-4-posts",
        "title": "General Blog (4 Posts)",
        "description": "4 short-to-medium articles on current personal finance topics, news reactions",
        "focus_keywords": "kewangan Malaysia, duit, budget, gaji, pelaburan"
    },
    {
        "id": "trends-to-article",
        "title": "Trends-to-Article",
        "description": "Read Google Trends Malaysia data and write 1 article on trending topic",
        "focus_keywords": "trending Malaysia, viral, berita terkini"
    },
]

def pick_next():
    """Pick next topic in round-robin, update state."""
    state = {"index": 0, "last_run": None, "history": []}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
        except:
            pass

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    next_idx = state.get("index", 0)

    # Safety: if index is out of range, reset
    if next_idx >= len(TOPICS):
        next_idx = 0

    topic = TOPICS[next_idx]

    # Update state
    state["index"] = (next_idx + 1) % len(TOPICS)
    state["last_run"] = now
    if "history" not in state:
        state["history"] = []
    state["history"].append({"topic": topic["id"], "date": now})
    # Keep last 30 entries
    state["history"] = state["history"][-30:]

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return topic, state

def main():
    topic, state = pick_next()

    # Build the output — this becomes the cron context
    output = f"""TOPIC_ROTATION
Today's topic: {topic['title']}
Topic ID: {topic['id']}
Description: {topic['description']}
Focus keywords: {topic['focus_keywords']}
Rotation index: {(state['index'] - 1) % len(TOPICS)} (next will be {state['index']})
Last 5 topics: {', '.join(h['topic'] for h in state['history'][-5:])}
"""
    sys.stdout.write(output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"TOPIC_ROTATION_ERROR: {e}\n")
        sys.exit(1)
