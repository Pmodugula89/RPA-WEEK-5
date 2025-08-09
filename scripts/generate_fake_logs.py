import logging
import time
import random
import psutil
from prometheus_client import start_http_server, Counter, Gauge
from datetime import datetime, timedelta
import json
# === Monitoring Strategy ===
# Configure structured JSON logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "function": record.funcName,
            "line_no": record.lineno,
        }
        return json.dumps(log_record)
logger = logging.getLogger("inventory_bot")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# Prometheus metrics
TRANSACTIONS_PROCESSED = Counter('transactions_processed_total', 'Total transactions processed')
TRANSACTION_ERRORS = Counter('transaction_errors_total', 'Total transaction errors')
CPU_USAGE_GAUGE = Gauge('cpu_usage_percent', 'System CPU usage percentage')
MEMORY_USAGE_GAUGE = Gauge('memory_usage_percent', 'System Memory usage percentage')
RETRIES_COUNTER = Counter('transaction_retries_total', 'Total retries on transactions')
# Start metrics HTTP server for Prometheus to scrape
start_http_server(8000)
def emit_system_metrics():
    CPU_USAGE_GAUGE.set(psutil.cpu_percent(interval=None))
    MEMORY_USAGE_GAUGE.set(psutil.virtual_memory().percent)
# === Transaction Processing with retry and logging ===
def process_transaction(transaction_id):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Simulated transient failure chance
            if random.random() < 0.3:
                raise Exception("Transient error occurred")
            # On success
            TRANSACTIONS_PROCESSED.inc()
            logger.info(f"Processed transaction {transaction_id} successfully")
            return True
        except Exception as e:
            TRANSACTION_ERRORS.inc()
            RETRIES_COUNTER.inc()
            logger.error(f"Error on transaction {transaction_id}, attempt {attempt+1}: {e}")
            time.sleep(2 ** attempt)  # exponential backoff
    logger.error(f"Transaction {transaction_id} failed after {max_retries} retries")
    # Here you might enqueue for dead-letter queue processing
    return False
# === Synthetic data generator for metrics simulation ===
def generate_synthetic_metrics(num_transactions=10000):
    baseline_time = datetime.utcnow()
    records = []
    for i in range(num_transactions):
        success = random.random() > 0.05  # 5% failure rate
        cpu_seconds = 0.05 if success else 0.1
        retries = 0 if success else random.randint(1, 3)
        records.append({
            "transaction_id": i,
            "timestamp": (baseline_time + timedelta(seconds=i * 0.1)).isoformat() + "Z",
            "success": success,
            "cpu_seconds": cpu_seconds,
            "retries": retries
        })
    return records
# === Example usage: run a few transactions and emit system metrics ===
if __name__ == "__main__":
    for tid in range(20):
        process_transaction(tid)
        emit_system_metrics()
        time.sleep(0.5)
