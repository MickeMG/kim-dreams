#!/usr/bin/env python3
"""
update_dream.py — Lägg till en ny dröm i dreams.json
Används av kim-dreams-nightly cron-job efter varje dröm.

Usage:
  python3 update_dream.py \
    --date 2026-03-02 \
    --title "Titeln" \
    --type "Surrealistisk dröm" \
    --mood "🌀" \
    --text "Drömtexten här." \
    --interpretation "Tolkningetexten." \
    --image "images/2026-03-02-dream.png" \
    --lucid false \
    --sleep-phase "REM 03:00-04:00"
"""

import argparse
import json
import os
from datetime import datetime

DREAMS_FILE = os.path.join(os.path.dirname(__file__), "dreams.json")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--mood", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--interpretation", required=True)
    p.add_argument("--image", default=None)
    p.add_argument("--lucid", default="false")
    p.add_argument("--sleep-phase", default="REM 03:00-04:00")
    args = p.parse_args()

    # Load existing
    with open(DREAMS_FILE, "r", encoding="utf-8") as f:
        dreams = json.load(f)

    # Build unique ID
    date_dreams = [d for d in dreams if d["date"] == args.date]
    letters = "abcdefghijklmnopqrstuvwxyz"
    idx = letters[len(date_dreams)] if len(date_dreams) < len(letters) else str(len(date_dreams))
    dream_id = f"{args.date}-{idx}"

    image = None if args.image in (None, "null", "") else args.image
    lucid = args.lucid.lower() in ("true", "1", "yes")

    new_dream = {
        "id": dream_id,
        "date": args.date,
        "type": getattr(args, "type"),
        "mood": args.mood,
        "title": args.title,
        "text": args.text,
        "interpretation": args.interpretation,
        "image": image,
        "lucid": lucid,
        "sleep_phase": getattr(args, "sleep_phase")
    }

    dreams.append(new_dream)

    with open(DREAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(dreams, f, indent=2, ensure_ascii=False)

    print(f"✅ Lade till dröm '{dream_id}': {args.title}")
    print(f"   Totalt {len(dreams)} drömmar i drömdagboken.")

if __name__ == "__main__":
    main()
