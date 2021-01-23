from django.urls import Path
from app.views import awaken, drink_selected

urlpatterns = [
    path("wake", awaken),
    path("selection/", drink_selected)
]