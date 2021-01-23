from django.urls import path
from app.views import awaken, drink_selected

urlpatterns = [
    path("wake", awaken),
    path("selection/", drink_selected)
]