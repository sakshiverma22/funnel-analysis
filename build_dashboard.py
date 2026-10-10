"""Refresh the embedded metrics in the dark dashboard without changing its layout."""
from pathlib import Path
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "dashboard" / "index.html"

def main():
    summary = pd.read_csv(ROOT / "data" / "funnel_summary_metrics.csv").iloc[0].to_dict()
    segments = pd.read_csv(ROOT / "data" / "segment_funnel_metrics.csv").to_dict("records")
    opportunities = pd.read_csv(ROOT / "data" / "opportunity_priorities.csv").to_dict("records")
    events = pd.read_csv(ROOT / "data" / "ecommerce_user_events.csv")
    payload = {"summary": summary, "segments": segments, "opportunities": opportunities,
               "revenue": float(events["order_value"].fillna(0).sum()),
               "avg_order_value": float(events["order_value"].dropna().mean())}
    text = INDEX.read_text(encoding="utf-8")
    replacement = "const data=" + json.dumps(payload, separators=(",", ":")) + "; const s=data.summary;"
    text, count = re.subn(r"const data=\{.*?\}; const s=data\.summary;", replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not find the dashboard data block")
    INDEX.write_text(text, encoding="utf-8")
    print(f"Dashboard refreshed: {INDEX}")

if __name__ == "__main__":
    main()
