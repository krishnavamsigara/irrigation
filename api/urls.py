from django.urls import path
from .views import GetRecommendations

urlpatterns = [
    path('recommend/', GetRecommendations.as_view()),
]
