#!/usr/bin/env python3
"""
generate_fake_logs.py
Creates synthetic bot logs (JSONL). Usage:
  python scripts/generate_fake_logs.py --rows 10000 --seed 12345 --out /data/synthetic_logs_10000.jsonl

Assumptions:
 - Transaction arrival: uniform spread across time range (adjustable)
 - Success rate: 98%, Retry rate: 1.5%, Fail rate: 0.5%
 - Duration: log-normal distribution with mean ~0.08s, sigma 0.5
 - Time range: Now - 24 hours
"""
import argparse, random, json, os, math
from datetime import datetime, timedelta
import numpy as np

def generate_row(ts, seed, idx, success_prob=0.98, retry_prob=0.015):
    r = random.random()
    if r < success_prob:
        status = "success"
        error_code = None
        retry_count = 0
    elif r < success_prob + retry_prob:
        status = "retry"
        error_code = "TRANSIENT_ERR"
        retry_count = random.choices([1,2,3], weights=[0.7,0.2,0.1])[0]
    else:
        status = "failed"
        error_code = "PERM_ERR"
        retry_count = random.randint(0,1)

    # duration in ms: lognormal
    duration_s = float(np.random.lognormal(mean=math.log(0.08), sigma=0.5))
    duration_ms = duration_s * 1000.0

    row = {
        "synthetic": True,
        "seed": seed,
        "timestamp": ts.isoformat() + "Z",
        "transaction_id": f"txn_{idx:07d}",
        "status": status,
        "duration_ms": round(duration_ms, 3),
        "error_code": error_code,
        "retry_count": retry_count,
        "worker_id": f"bot-{random.randint(1,8)}",
        "function": "process_batch",
        "line": 312,
        "payload_size": random.randint(256, 4096)
    }
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--out", type=str, default="/data/synthetic_logs_10000.jsonl")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    now = datetime.utcnow()
    start = now - timedelta(hours=24)

    with open(args.out, "w", encoding="utf-8") as fh:
        for i in range(args.rows):
            frac = i / max(1, args.rows - 1)
            ts = start + timedelta(seconds=frac * 24 * 3600) \
                 + timedelta(seconds=random.uniform(-1, 1))
            row = generate_row(ts, args.seed, i+1)
            fh.write(json.dumps(row))
            fh.write("\\n")

    print(f"Wrote {args.rows} synthetic log rows to {args.out} (seed={args.seed})")

if __name__ == "__main__":
    main()
