from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import NotificationLog, PriceAlert

class PriceThresholdTest(TestCase):
    def test_threshold_boundaries(self):
        self.assertTrue(4200 <= 4500)
        self.assertTrue(4500 <= 4500)
        self.assertFalse(5000 <= 4500)

class NotificationLogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.alert = PriceAlert.objects.create(user=self.user, origin="DEL", destination="BOM", threshold_price=4500)
    def test_notification_log_is_created_with_correct_data(self):
        log = NotificationLog.objects.create(alert=self.alert, triggered_price=4200, message="Price dropped to 4200 for DEL-BOM")
        self.assertEqual(log.triggered_price, 4200)
        self.assertEqual(log.alert, self.alert)
        self.assertIn("DEL-BOM", log.message)

class AlertScopingTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username="user1", password="pass")
        self.user2 = get_user_model().objects.create_user(username="user2", password="pass")
        PriceAlert.objects.create(user=self.user1, origin="DEL", destination="BOM", threshold_price=4500)
        PriceAlert.objects.create(user=self.user2, origin="BLR", destination="HYD", threshold_price=2000)
    def test_user_only_sees_own_alerts(self):
        alerts = PriceAlert.objects.filter(user=self.user1)
        self.assertEqual(alerts.count(), 1)
        self.assertEqual(alerts.first().origin, "DEL")
