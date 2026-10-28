"""Non-executing starter dashboard for the Trading Agent project.

This application uses only the Python standard library. All displayed market
values are fictional demo data. It does not fetch prices or place orders.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("TRADING_AGENT_HOST", "127.0.0.1")
PORT = int(os.environ.get("TRADING_AGENT_PORT", "8000"))


def get_status() -> dict[str, Any]:
    """Return safe, explicit application status without connecting externally."""
    return {
        "application": "Trading Agent",
        "status": "running",
        "mode": "demo",
        "execution_enabled": False,
        "broker_connected": False,
        "market_data_source": "fictional demo data",
        "message": "Demo mode only. No live prices, broker connection, or orders.",
    }


def get_demo_market_data() -> dict[str, Any]:
    """Return clearly labelled sample values; these are not current prices."""
    return {
        "is_demo_data": True,
        "updated_at": "Sample data — not a live timestamp",
        "instruments": [
            {"symbol": "EUR/USD", "price": 1.0842, "change_percent": 0.24},
            {"symbol": "GBP/USD", "price": 1.2718, "change_percent": -0.11},
            {"symbol": "USD/JPY", "price": 149.32, "change_percent": 0.08},
        ],
    }


def render_dashboard() -> bytes:
    """Read the dashboard HTML from disk so it can be edited independently."""
    return (ROOT / "index.html").read_bytes()


class TradingAgentHandler(BaseHTTPRequestHandler):
    server_version = "TradingAgentDemo/0.1"

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        path = urlparse(self.path).path
        if path == "/":
            try:
                self._send(200, render_dashboard(), "text/html; charset=utf-8")
            except OSError:
                self._send(500, b"Dashboard file could not be read.", "text/plain; charset=utf-8")
        elif path == "/health":
            self._send(200, b'{"status":"ok"}', "application/json; charset=utf-8")
        elif path == "/api/status":
            body = json.dumps(get_status()).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        elif path == "/api/market-data":
            body = json.dumps(get_demo_market_data()).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        else:
            self._send(404, b'{"error":"not_found"}', "application/json; charset=utf-8")

    def log_message(self, format: str, *args: Any) -> None:
        # Keep local development output concise; HTTP errors are still returned.
        print("%s - %s" % (self.address_string(), format % args))


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), TradingAgentHandler)
    print(f"Trading Agent demo dashboard: http://{HOST}:{PORT}")
    print("Safety: demo mode; no live market data, broker connection, or order execution.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Trading Agent dashboard...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
