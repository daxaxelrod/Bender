from django.urls import path
from app.views import awaken, drinks

urlpatterns = [
    path("wake/", awaken),
    path("drinks/", drinks)
]