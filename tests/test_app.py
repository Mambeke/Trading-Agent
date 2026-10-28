"""Tests for the Trading Agent's non-executing starter foundation."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from app import TradingAgentHandler, get_demo_market_data, get_status


class StatusTests(unittest.TestCase):
    def test_status_is_explicitly_non_executing(self):
        status = get_status()
        self.assertEqual(status["status"], "running")
        self.assertEqual(status["mode"], "demo")
        self.assertFalse(status["execution_enabled"])
        self.assertFalse(status["broker_connected"])

    def test_market_data_is_marked_as_demo(self):
        data = get_demo_market_data()
        self.assertTrue(data["is_demo_data"])
        self.assertEqual(
            [item["symbol"] for item in data["instruments"]],
            ["EUR/USD", "GBP/USD", "USD/JPY"],
        )
        self.assertTrue(all(item["price"] > 0 for item in data["instruments"]))


class HttpEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), TradingAgentHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get_json(self, path):
        with urlopen(self.base_url + path, timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("application/json", response.headers["Content-Type"])
            return json.loads(response.read().decode("utf-8"))

    def test_health_endpoint(self):
        self.assertEqual(self.get_json("/health"), {"status": "ok"})

    def test_status_endpoint_keeps_execution_disabled(self):
        self.assertFalse(self.get_json("/api/status")["execution_enabled"])

    def test_market_data_endpoint_marks_values_as_demo(self):
        self.assertTrue(self.get_json("/api/market-data")["is_demo_data"])

    def test_unknown_route_returns_404(self):
        from urllib.error import HTTPError
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base_url + "/not-a-route", timeout=2)
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
