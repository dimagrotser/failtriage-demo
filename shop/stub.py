"""A stand-in for the rates service, so the tests need no network: python -m shop.stub"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

RATES = {"EUR": 0.9, "GBP": 0.8}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = json.dumps(RATES).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8099), Handler).serve_forever()
