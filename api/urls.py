from django.urls import path

from . import views

urlpatterns = [
    path('add_job', views.add_job),
]
