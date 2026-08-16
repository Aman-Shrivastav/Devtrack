import random
from django.contrib.auth import authenticate
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import NotificationLog, PriceAlert
from .permissions import IsAdminUser
from .serializers import PriceAlertSerializer, RegisterSerializer

MOCK_PRICES = {"DEL-BOM": (3000, 7000), "BLR-HYD": (1500, 4000), "DEL-BLR": (4000, 9000), "BOM-GOA": (2000, 5000)}

def token_for(user):
    return str(RefreshToken.for_user(user).access_token)

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"username": user.username, "access": token_for(user), "role": user.profile.role}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"username": user.username, "access": token_for(user), "role": user.profile.role})

class AlertListCreateView(APIView):
    def get(self, request):
        return Response(PriceAlertSerializer(PriceAlert.objects.filter(user=request.user), many=True).data)
    def post(self, request):
        serializer = PriceAlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(PriceAlertSerializer(serializer.save(user=request.user)).data, status=status.HTTP_201_CREATED)

class AlertDeactivateView(APIView):
    def delete(self, request, pk):
        alert = get_object_or_404(PriceAlert, id=pk)
        if alert.user_id != request.user.id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        alert.status = PriceAlert.Status.INACTIVE
        alert.save(update_fields=["status"])
        return Response({"status": PriceAlert.Status.INACTIVE})

def get_flight_price(request):
    route = request.GET.get("route", "").upper()
    price_range = MOCK_PRICES.get(route)
    if not price_range:
        return JsonResponse({"error": "Route not found"}, status=404)
    return JsonResponse({"route": route, "price": random.randint(*price_range)})

class AdminSummaryView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        counts = PriceAlert.objects.aggregate(total_alerts=Count("id"), active_alerts=Count("id", filter=Q(status=PriceAlert.Status.ACTIVE)), triggered_alerts=Count("id", filter=Q(status=PriceAlert.Status.TRIGGERED)))
        top_routes = PriceAlert.objects.values("origin", "destination").annotate(alert_count=Count("id")).order_by("-alert_count", "origin", "destination")[:5]
        return Response({**counts, "total_notifications": NotificationLog.objects.aggregate(total=Count("id"))["total"], "top_routes": [{"route": f"{item['origin']}-{item['destination']}", "alert_count": item["alert_count"]} for item in top_routes]})
