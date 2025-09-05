from datetime import timedelta
from .models import TeaLogs

def check_drink_count():
    """차 마시기 로그(TeaLog) 횟수를 반환합니다."""
    return TeaLogs.objects.all().count()

def check_record_count():
    """코멘트(comment)가 남겨진 기록의 총 횟수를 반환합니다."""
    return TeaLogs.objects.exclude(comment__exact='').count()

def check_unique_tea_count():
    """기록된 서로 다른 종류의 차(Tea) 개수를 반환합니다."""
    return TeaLogs.objects.values('tea_id').distinct().count()

def check_consecutive_days():
    """기록 중 최장 연속 차 마신 일수를 계산합니다."""
    dates = TeaLogs.objects.dates('created_at', 'day', order='DESC')
    
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