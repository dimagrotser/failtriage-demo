import json
import os
import urllib.request


def rate(currency: str) -> float:
    base = os.environ.get("RATES_URL", "http://127.0.0.1:8099")
    with urllib.request.urlopen(f"{base}/rates", timeout=2) as response:
        return json.load(response)[currency]


def convert(cents: int, currency: str) -> int:
    return round(cents * rate(currency))
