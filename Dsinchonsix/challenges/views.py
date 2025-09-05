from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Challenge
from .checkers import CHALLENGE_CHECKERS

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