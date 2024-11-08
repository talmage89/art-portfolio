from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class APIPermissionsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_access(self):
        # should allow
        response = self.client.get("/api/artworks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/api/images/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # should reject
        response = self.client.post("/api/artworks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post("/api/images/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # should not exist
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get("/api/payments/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post("/api/payments/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
