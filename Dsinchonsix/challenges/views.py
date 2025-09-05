from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Challenge, UserChallenge
from .checkers import CHALLENGE_CHECKERS

# 챌린지별 목표치를 코드로 정의합니다.
CHALLENGE_GOALS = {
    'DRINK_COUNT': 5,
    'RECORD_COUNT': 10,
    'UNIQUE_TEA_COUNT': 5,
    'CONSECUTIVE_DAYS': 3,
}

class ChallengeStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        all_challenges = Challenge.objects.all()
        user_completed_challenges = UserChallenge.objects.filter(user=user, is_completed=True).values_list('challenge_id', flat=True)

        response_data = []
        for challenge in all_challenges:
            checker_function = CHALLENGE_CHECKERS.get(challenge.challenge_type)
            
            current_progress = 0
            if checker_function:
                current_progress = checker_function(user)

            goal = CHALLENGE_GOALS.get(challenge.challenge_type, 0)

            response_data.append({
                'id': challenge.id,
                'title': challenge.title,
                'description': challenge.description,
                'goal': goal,
                'current_progress': current_progress,
                'is_completed': challenge.id in user_completed_challenges,
            })
            
        return Response(response_data)