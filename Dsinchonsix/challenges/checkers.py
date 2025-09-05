from datetime import timedelta
# TeaLog 모델의 실제 경로에 맞게 수정해주세요.
# 여기서는 'apps.tealogs.models'에 'TeaLog' 모델이 있다고 가정합니다.
from .models import TeaLogs

def check_drink_count(user):
    """사용자가 마신 차의 총 로그(TeaLog) 횟수를 반환합니다."""
    return TeaLogs.objects.filter(user=user).count()

def check_record_count(user):
    """사용자가 코멘트(comment)를 남긴 기록의 총 횟수를 반환합니다."""
    # comment 필드가 비어있지 않은 로그의 개수를 셉니다.
    return TeaLogs.objects.filter(user=user).exclude(comment__exact='').count()

def check_unique_tea_count(user):
    """사용자가 마신 서로 다른 종류의 차(Tea) 개수를 반환합니다."""
    return TeaLogs.objects.filter(user=user).values('tea_id').distinct().count()

def check_consecutive_days(user):
    """사용자의 최장 연속 차 마신 일수를 계산합니다."""
    # 사용자의 모든 로그 날짜를 중복 없이, 최신순으로 가져옵니다.
    dates = TeaLogs.objects.filter(user=user).dates('created_at', 'day', order='DESC')
    
    if not dates:
        return 0

    longest_streak = 0
    current_streak = 1
    
    for i in range(len(dates) - 1):
        if dates[i] - dates[i+1] == timedelta(days=1):
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
            
    longest_streak = max(longest_streak, current_streak)
    
    return longest_streak

# 챌린지 타입과 검사 함수를 딕셔너리로 매핑
CHALLENGE_CHECKERS = {
    'DRINK_COUNT': check_drink_count,
    'RECORD_COUNT': check_record_count,
    'UNIQUE_TEA_COUNT': check_unique_tea_count,
    'CONSECUTIVE_DAYS': check_consecutive_days,
}