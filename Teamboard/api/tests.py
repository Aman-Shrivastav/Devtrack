from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Company, KBEntry, QueryLog


class TeamBoardAPITests(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user("client", password="securepass123")
        self.client_company = self.client_user.company
        self.client_company.company_name = "Client Co"
        self.client_company.save()

        self.admin_user = User.objects.create_user("admin", password="securepass123")
        self.admin_user.company.company_name = "Admin Co"
        self.admin_user.company.role = Company.Role.ADMIN
        self.admin_user.company.save()

        self.matching_entry = KBEntry.objects.create(
            question="What is select_related?",
            answer="select_related fetches a related object with a SQL join.",
            category=KBEntry.Category.DATABASE,
        )

    def test_register_creates_client_company_and_returns_credentials(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "acmecorp",
                "password": "securepass123",
                "company_name": "Acme Corp",
                "email": "dev@acme.test",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["access"])
        company = Company.objects.get(user__username="acmecorp")
        self.assertEqual(company.company_name, "Acme Corp")
        self.assertEqual(company.role, Company.Role.CLIENT)
        self.assertTrue(company.api_key)

    def test_register_rejects_duplicate_username(self):
        response = self.client.post(
            reverse("register"),
            {"username": "client", "password": "securepass123", "company_name": "Duplicate", "email": "x@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "client", "password": "securepass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Client Co")
        self.assertEqual(response.data["api_key"], self.client_company.api_key)

    def test_login_rejects_bad_credentials(self):
        response = self.client.post(reverse("login"), {"username": "client", "password": "wrong"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_query_requires_authentication(self):
        response = self.client.post(reverse("kb-query"), {"search": "select"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_query_searches_and_logs_result(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.post(reverse("kb-query"), {"search": "select_related"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.matching_entry.id)
        log = QueryLog.objects.get()
        self.assertEqual(log.company, self.client_company)
        self.assertEqual(log.results_count, 1)

    def test_query_logs_zero_result_searches(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.post(reverse("kb-query"), {"search": "not-found"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(QueryLog.objects.get().results_count, 0)

    def test_query_rejects_blank_search(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.post(reverse("kb-query"), {"search": " "}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_usage_summary_rejects_client(self):
        self.client.force_authenticate(self.client_user)
        response = self.client.get(reverse("usage-summary"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_usage_summary_aggregates_queries(self):
        QueryLog.objects.create(company=self.client_company, search_term="select_related", results_count=1)
        QueryLog.objects.create(company=self.client_company, search_term="select_related", results_count=1)
        QueryLog.objects.create(company=self.admin_user.company, search_term="JWT", results_count=0)

        self.client.force_authenticate(self.admin_user)
        response = self.client.get(reverse("usage-summary"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_queries"], 3)
        self.assertEqual(response.data["active_companies"], 2)
        self.assertEqual(response.data["top_search_terms"][0], {"search_term": "select_related", "count": 2})
