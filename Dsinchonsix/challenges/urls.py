from django.urls import path
from .views import *

urlpatterns = [
    path('challenges/log/', TeaLogCreateView.as_view(), name='tea-log-create'),
]
