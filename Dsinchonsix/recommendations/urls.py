from django.urls import path
from .views import TeaByMoodView, TeaView

app_name = "recommendations"

urlpatterns = [
    path("filter/mood/", TeaByMoodView.as_view(), name="mood-api"), #카테고리 필터링
    path("filter/taste/", TeaView.as_view(), name="taste-api"), #맛 필터링
    # path() #
]
