from django.shortcuts import render
from teas.models import Tea, TeaCategory
from rest_framework.views import APIView
from .serializers import TeaSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

#기분 카테고리 필터링 뷰
class TeaByMoodView(APIView):
    def get(self, request):
        mood = request.query_params.get("mood")
        if not mood:
            return Response({"detail":"mood required"}, status=400)

        qs = Tea.objects.select_related("tea_category")\
                        .filter(tea_category__mood=mood)

        # 이 mood에서 고를 수 있는 taste 후보만 추림
        tastes = qs.values("taste_id", "taste").distinct().order_by("taste_id")
        return Response({
            "tastes": [{"id": t["taste_id"], "label": t["taste"]} for t in tastes]
        }, status=200)


#기분+맛 최종 필터랑 뷰
class TeaView(APIView):
    def get(self, request):
        taste_id = request.query_params.get("taste_id")
        if not taste_id:
            return Response({"detail": "taste_id required"}, status=status.HTTP_400_BAD_REQUEST)

        tea = (Tea.objects.select_related("tea_category")
               .filter(taste_id=taste_id)
               .first())

        if not tea:
            return Response({"detail": "no tea found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"tea": TeaSerializer(tea).data}, status=status.HTTP_200_OK)
