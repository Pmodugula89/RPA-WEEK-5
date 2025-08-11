#!/usr/bin/env python3
from prometheus_client import start_http_server, Counter, Histogram
import time, random

INV_TRANSACTIONS = Counter('inv_transactions_total', 'Inventory transactions', ['status'])
INV_RETRIES = Counter('inv_retries_total', 'Inventory retries')
INV_LATENCY = Histogram('inv_batch_seconds', 'Inventory batch duration seconds')

@INV_LATENCY.time()
def process_batch():
    time.sleep(random.uniform(0.04, 0.2))
    if random.random() < 0.98:
        INV_TRANSACTIONS.labels(status="success").inc()
    else:
        INV_TRANSACTIONS.labels(status="failed").inc()

if __name__ == "__main__":
    start_http_server(9100)
    while True:
        process_batch()
        if random.random() < 0.01:
            INV_RETRIES.inc()
