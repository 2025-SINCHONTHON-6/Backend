from django.urls import path
from .views import *

app_name = 'challenges'

urlpatterns = [
    path('log/', TeaLogCreateView.as_view(), name='tea-log-create'),
    path('status/', ChallengeStatusView.as_view(), name='challenge-status'),
    path('recommendations/recent/', RecentRecommendedTeaView.as_view(), name='recent-recommendation'),
    path('records/daily/', MyTeaLogByDateView.as_view(), name='mytealog')
]