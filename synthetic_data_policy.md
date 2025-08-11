# Synthetic Data Policy

This document defines rules for generating and using synthetic telemetry for monitoring, ROI, and scaling analysis. See included scripts for generation and verification.

**Key rules:**
- No real production data
- Store generated data under `/data/`
- Include metadata files with `synthetic: true` and seed
- Document assumptions in metadata and docs

See `/scripts/generate_fake_logs.py` and `/scripts/verify_synthetic.py` for examples.
