import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


class TestApp(unittest.TestCase):

    @patch("services.balances.get_balances")
    def test_get_balance_valid_address(self, mock_get_balances):
        mock_get_balances.return_value = (100, 200)

        payload = {"wallet_address": "0x7a16ff8270133f063aab6c9977183d9e72835428"}
        response = client.post("/v1/get_balance/", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("wallet_address", data)
        self.assertIn("last_update", data)
        self.assertIn("token_balance", data)
        self.assertIn("usd_balance", data)

    def test_get_balance_invalid_address(self):
        payload = {"wallet_address": "invalid_address"}
        response = client.post("/v1/get_balance/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_history_valid_wallet(self):
        wallet_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        response = client.get(f"/v1/get_history/?wallet_address={wallet_address}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn("timestamp", entry)
            self.assertIn("token_balance", entry)
            self.assertIn("usd_balance", entry)

    def test_get_history_invalid_wallet(self):
        invalid_wallet = "invalid_wallet"
        response = client.get(f"/v1/get_history/?wallet_address={invalid_wallet}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main()
