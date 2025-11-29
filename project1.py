import requests
import time
from datetime import datetime
import csv
import sys

BASE_URL = "https://api.binance.com"
TICKER_ENDPOINT = "/api/v3/ticker/price"  

SYMBOL = "BTCUSDT"        
POLL_INTERVAL = 120      
CSV_OUTPUT = "price_log.csv"  

def get_price(symbol: str) -> float:
    """Return current price for symbol from Binance public API."""
    url = f"{BASE_URL}{TICKER_ENDPOINT}"
    params = {"symbol": symbol}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data["price"])
def percent_change(prev: float, curr: float) -> float:
    if prev == 0:
        return 0.0
    return (curr - prev) / prev * 100.0

def main():
    samples = [] 
    header_written = False

    csvfile = None
    csvwriter = None
    if CSV_OUTPUT:
        csvfile = open(CSV_OUTPUT, mode="a", newline="")
        csvwriter = csv.writer(csvfile)
        try:
            csvfile.seek(0)
            if csvfile.read(1) == "":
                csvfile.seek(0)
                csvwriter.writerow(["timestamp_iso", "timestamp_unix", "symbol", "price"])
        except Exception:
            pass

    print(f"Starting Binance poller for symbol {SYMBOL}. Poll every {POLL_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            ts = datetime.utcnow()
            try:
                price = get_price(SYMBOL)
            except requests.RequestException as e:
                print(f"[{ts.isoformat()}] Network/API error: {e}. Will retry in next interval.")
                time.sleep(POLL_INTERVAL)
                continue
            samples.append((ts, price))
            if csvwriter:
                csvwriter.writerow([ts.isoformat(), int(ts.timestamp()), SYMBOL, price])
                csvfile.flush()

            prices = [p for (_, p) in samples]
            min_price = min(prices)
            max_price = max(prices)

            pct_changes = []
            for i in range(1, len(prices)):
                pct = percent_change(prices[i-1], prices[i])
                pct_changes.append(pct)
                       
            if pct_changes:
                max_fly = max(pct_changes) 
                min_fly = min(pct_changes) 
            else:
                max_fly = 0.0
                min_fly = 0.0

            print(f"[{ts.isoformat()}] {SYMBOL} price: {price:.8f}")
            print(f"   min price so far: {min_price:.8f}")
            print(f"   max price so far: {max_price:.8f}")
            print(f"   samples collected: {len(samples)}")
            print(f"   max fly (biggest % increase between consecutive samples): {max_fly:.6f}%")
            print(f"   min fly (biggest % decrease between consecutive samples): {min_fly:.6f}%")
            print("-" * 60)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping poller (Ctrl+C received).")
    finally:
        if csvfile:
            csvfile.close()
        if CSV_OUTPUT:
            print(f"Saved samples to {CSV_OUTPUT}")
if __name__ == "__main__":
    main()
