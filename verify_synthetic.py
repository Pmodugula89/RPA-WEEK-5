#!/usr/bin/env python3
"""
verify_synthetic.py
Verifies synthetic JSONL files and produces /data/summary.json
Usage:
  python scripts/verify_synthetic.py --in /data/synthetic_logs_10000.jsonl --meta /data/synthetic_logs_10000.jsonl.meta.json
"""
import argparse, json, sys, os
from statistics import mean, median
def load_meta(meta_path):
    with open(meta_path) as f:
        return json.load(f)
def analyze(in_path):
    counts = {"rows":0, "success":0, "failed":0, "retry":0, "duration_ms":[]}
    with open(in_path) as fh:
        for line in fh:
            if not line.strip(): continue
            obj = json.loads(line)
            if not obj.get("synthetic", False):
                raise ValueError("File contains non-synthetic record")
            counts["rows"] += 1
            st = obj.get("status")
            if st == "success": counts["success"] += 1
            elif st == "failed": counts["failed"] += 1
            elif st == "retry": counts["retry"] += 1
            counts["duration_ms"].append(obj.get("duration_ms", 0))
    return counts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", required=True)
    parser.add_argument("--meta", dest="meta", required=True)
    args = parser.parse_args()
    if not os.path.exists(args.infile):
        print("Input file not found:", args.infile); sys.exit(2)
    meta = load_meta(args.meta)
    counts = analyze(args.infile)
    if counts["rows"] != meta.get("rows"):
        print("Row count mismatch! meta rows:", meta.get("rows"), "actual:", counts["rows"])
    summary = {
        "meta": meta,
        "actual_rows": counts["rows"],
        "success": counts["success"],
        "failed": counts["failed"],
        "retry": counts["retry"],
        "avg_duration_ms": mean(counts["duration_ms"]) if counts["duration_ms"] else None,
        "median_duration_ms": median(counts["duration_ms"]) if counts["duration_ms"] else None
    }
    out = "/data/summary.json"
    with open(out, "w") as fh:
        json.dump(summary, fh, indent=2)
    print("Wrote summary to", out)

if __name__ == "__main__":
    main()
