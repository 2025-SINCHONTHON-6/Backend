from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from .checkers import CHALLENGE_CHECKERS
from rest_framework.response import Response

# 챌린지별 목표치를 코드로 정의
CHALLENGE_GOALS = {
    'DRINK_COUNT': 5,
    'RECORD_COUNT': 10,
    'UNIQUE_TEA_COUNT': 5,
    'CONSECUTIVE_DAYS': 3,
}

class ChallengeStatusView(APIView):

    def get(self, request):
        all_challenges = Challenge.objects.all()

        response_data = []
        for challenge in all_challenges:
            checker_function = CHALLENGE_CHECKERS.get(challenge.challenge_type)
            
            current_progress = 0
            if checker_function:
                current_progress = checker_function()

            goal = CHALLENGE_GOALS.get(challenge.challenge_type, 0)
            
            is_completed = current_progress >= goal

            response_data.append({
                'id': challenge.id,
                'title': challenge.title,
                'description': challenge.description,
                'goal': goal,
                'current_progress': current_progress,
                'is_completed': is_completed,
            })
            
        return Response(response_data)

class TeaLogCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            recent = RecentRecommendedTea.objects.latest('created_at')
        except RecentRecommendedTea.DoesNotExist:
            return Response({"error": "최근 추천된 차가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['tea_id'] = recent.tea.id  # tea_id 강제 세팅

        serializer = TeaLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class RecentRecommendedTeaView(APIView):
    def post(self, request):
        tea_id = request.data.get("tea_id")
        tea = Tea.objects.get(id=tea_id)
        RecentRecommendedTea.objects.all().delete()
        RecentRecommendedTea.objects.create(tea=tea)
        return Response({"status": "ok"})
    
    def get(self, request):
        try:
            recent = RecentRecommendedTea.objects.latest('created_at')
            return Response({"id": recent.tea.id, "name": recent.tea.name})
        except RecentRecommendedTea.DoesNotExist:
            return Response({"error": "No recent recommendation"}, status=404)