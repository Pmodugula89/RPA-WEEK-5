# Synthetic Telemetry Repo (Demo)

Local demo:
1. Generate synthetic logs: python scripts/generate_fake_logs.py --rows 10000 --seed 12345 --out /data/synthetic_logs_10000.jsonl
2. Verify: python scripts/verify_synthetic.py --in /data/synthetic_logs_10000.jsonl --meta /data/synthetic_logs_10000.jsonl.meta.json
3. Start demo metrics: python scripts/prometheus_instrumentation.py (exposes :9100)
4. Start logging demo: python scripts/logging_json_config.py

Files in repo:
- /scripts/
- /data/
- /docs/
- /diagrams/
