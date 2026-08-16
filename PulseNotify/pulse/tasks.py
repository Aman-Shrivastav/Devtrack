import requests
from celery import shared_task
from .models import NotificationLog, PriceAlert

PRICE_FEED_URL = "http://localhost:8000/api/flights/price/"

@shared_task
def check_prices():
    active_alerts = PriceAlert.objects.filter(status=PriceAlert.Status.ACTIVE)
    for origin, destination in active_alerts.values_list("origin", "destination").distinct():
        response = requests.get(PRICE_FEED_URL, params={"route": f"{origin}-{destination}"}, timeout=10)
        if response.status_code != 200:
            continue
        current_price = response.json().get("price")
        for alert in active_alerts.filter(origin=origin, destination=destination):
            if current_price <= float(alert.threshold_price):
                send_notification.delay(alert.id, current_price)

@shared_task
def send_notification(alert_id, triggered_price):
    alert = PriceAlert.objects.get(id=alert_id)
    if alert.status != PriceAlert.Status.ACTIVE:
        return
    message = (f"Price alert triggered! {alert.origin}-{alert.destination} is now ₹{triggered_price} " f"- below your threshold of ₹{alert.threshold_price}")
    NotificationLog.objects.create(alert=alert, triggered_price=triggered_price, message=message)
    alert.status = PriceAlert.Status.TRIGGERED
    alert.save(update_fields=["status"])
