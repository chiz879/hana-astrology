import unittest
from fastapi.testclient import TestClient
from main import app

class TestAstrologyApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HANA", response.content)
        self.assertIn(b"CUSP TABLE", response.content)

    def test_calculate_endpoint_success(self):
        payload = {
            "birth_date": "2000-01-01",
            "birth_time": "12:00",
            "birth_place": "Tokyo",
            "house_system": "P"
        }
        response = self.client.post("/api/calculate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["status"], "success")
        self.assertIn("resolved_location", data)
        self.assertIn("data", data)
        
        # Check coordinates and timezone for Tokyo
        self.assertAlmostEqual(data["resolved_location"]["latitude"], 35.6768, places=1)
        self.assertAlmostEqual(data["resolved_location"]["longitude"], 139.7639, places=1)
        self.assertEqual(data["resolved_location"]["timezone"], "Asia/Tokyo")
        
        # Check computed values
        self.assertIn("asc", data["data"])
        self.assertIn("mc", data["data"])
        self.assertEqual(len(data["data"]["cusps"]), 12)
        
        # Check formatting of house 1 (should match ASC)
        self.assertEqual(data["data"]["cusps"][0]["formatted"], data["data"]["asc"]["formatted"])

    def test_calculate_endpoint_invalid_location(self):
        payload = {
            "birth_date": "2000-01-01",
            "birth_time": "12:00",
            "birth_place": "ThisLocationDoesNotExistOnEarth12345",
            "house_system": "P"
        }
        response = self.client.post("/api/calculate", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)

if __name__ == "__main__":
    unittest.main()
