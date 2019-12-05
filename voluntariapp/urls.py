# voluntariapp/urls.py
from django.urls import include, path
from . import views
from .views import login

urlpatterns = [
    path('login',login),

    path('event', views.EventListView.as_view()),
    path('event/<id_event>', views.EventDetailView.as_view(), name="event-details"),
]