from django.urls import path
from .views import mark_attendance_view

urlpatterns = [
    path('', mark_attendance_view, name='mark_attendance'),
]
