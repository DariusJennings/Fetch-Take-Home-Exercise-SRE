import argparse
import yaml
import requests
import time
import logging
from urllib.parse import urlparse
from threading import Thread

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# Global cumulative stats by domain
cumulative_stats = {}  # { domain: { total: int, available: int } }

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_domain(url):
    parsed = urlparse(url)
    return parsed.hostname

def check_endpoint(endpoint):
    method = endpoint.get("method", "GET").upper()
    url = endpoint["url"]
    headers = endpoint.get("headers", {})
    body = endpoint.get("body")
    name = endpoint.get("name", url)
    domain = get_domain(url)
    timeout = 0.5

    start = time.time()
    status_code = None
    available = False

    try:
        response = requests.request(method, url, headers=headers, data=body, timeout=timeout)
        latency = (time.time() - start) * 1000
        status_code = response.status_code
        available = 200 <= status_code <= 299 and latency <= 500
        log_status = "AVAILABLE" if available else "UNAVAILABLE"
        logging.info(f"[{name}] {url} - {log_status} | Status: {status_code} | Time: {latency:.2f}ms")
    except Exception as e:
        latency = (time.time() - start) * 1000
        logging.info(f"[{name}] {url} - UNAVAILABLE | Error: {str(e)} | Time: {latency:.2f}ms")

    # Track cumulative stats by domain
    if domain not in cumulative_stats:
        cumulative_stats[domain] = {"total": 0, "available": 0}
    cumulative_stats[domain]["total"] += 1
    if available:
        cumulative_stats[domain]["available"] += 1

def monitor(endpoints):
    while True:
        for endpoint in endpoints:
            check_endpoint(endpoint)

        # Log cumulative domain-level availability stats
        for domain, stats in cumulative_stats.items():
            total = stats["total"]
            available = stats["available"]
            pct = (available / total * 100) if total else 0
            logging.info(f"[CUMULATIVE] {domain} - Availability: {available}/{total} ({pct:.2f}%)")

        time.sleep(15)

def main():
    parser = argparse.ArgumentParser(description="Endpoint availability checker.")
    parser.add_argument("config", help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    if not config or not isinstance(config, list):
        logging.error("Invalid configuration format. Expecting a list of endpoint definitions.")
        return

    Thread(target=monitor, args=(config,), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully... Bye! 👋")

if __name__ == "__main__":
    main()
