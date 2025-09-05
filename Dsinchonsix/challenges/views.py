from rest_framework.views import APIView
from rest_framework.response import Response
from teas.models import *
from .serializers import *
from rest_framework import status
from .checkers import CHALLENGE_CHECKERS
from rest_framework.response import Response
from datetime import date

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
        

class MyTeaLogByDateView(APIView):
    """
    GET /api/my/log?date=2025-09-11
    응답: TeaLogSerializer 그대로 (tea, feeling, comment, created_at 포함)
    """
    def get(self, request):
        dstr = request.query_params.get("created_at")
        if not dstr:
            return Response({"detail": "created_at=YYYY-MM-DD 필요"}, status=400)
        try:
            d = date.fromisoformat(dstr)
        except ValueError:
            return Response({"detail": "created_at 형식 오류(YYYY-MM-DD)"}, status=400)

        log = (TeaLogs.objects
               .select_related("tea")          # 리뷰가 OneToOne이면 .select_related("review") 추가
               .filter(created_at=d)
               .order_by("-id")
               .first())
        if not log:
            return Response({"detail": "해당 날짜 기록 없음"}, status=404)

        return Response(TeaLogSerializer(log).data, status=200)


class TeaLogDateListView(APIView):
    def get(self, request):
        dates = TeaLogs.objects.order_by('-created_at').values_list('created_at', flat=True).distinct()
        dates = [date.strftime('%Y-%m-%d') for date in dates]
        return Response(dates)

