import requests
import datetime
import time

TOKEN = "8513262392:AAEH5OkiGB4cFUR3lLRb01admHVz9Jrb0yc"
CHAT_ID = "8250645779"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def get_week_of_month():
    today = datetime.date.today()
    first_day = today.replace(day=1)
    return (today.day + first_day.weekday()) // 7 + 1

# ✅ 주차 메시지
def weekly_message():
    week = get_week_of_month()

    if week == 1:
        return """[이번주 핵심: 세팅]
- 인스탁 수량 확인
- 시트 초기화
- 메이커스 정산 + ERP
- 익월 상품 제안 (~10일까지)
※ 이번주 꼬이면 한 달 꼬임"""

    elif week == 2:
        return """[이번주 핵심: 기획]
- 프로모션 초안 작성
- 쿠팡 목표 매출 체크
- MD 커뮤니케이션 시작
※ 자리 선점 중요"""

    elif week == 3:
        return """[이번주 핵심: 확정]
- 프로모션 확정
- 컬리/그립 제안
- 리오더 준비 (화요일 전 필수)
- 콘텐츠 요청
※ 매출 결정 구간"""

    else:
        return """[이번주 핵심: 마감]
- 반출 금액 계산
- 발주 준비
- 매입/이관 체크
※ 다음달 매출 결정"""

# ✅ 요일별 (시간 포함 풀버전)
def daily_message():
    weekday = datetime.datetime.today().weekday()

    messages = {
        0: """[월요일]

08:30~09:30
- 채널 점검
- 쿠팡 발주서 / 티켓 처리
- 매출 / 정산 확인

오전/오후
- 주간 방향 설정
- 밀린 업무 정리
- 행사 일정 체크

17:00~17:45
- 다음날 업무 정리
- 행사 공유""",

        1: """[화요일 - 리오더]

08:30~09:30
- 채널 점검
- 매출 확인

11:30
- 리오더 준비
- 재고 점검
- 입고 일정 확인

14:00 미팅
- 부족 수량 / 리스크 공유

17:00~17:45
- 다음날 정리

※ 재고 놓치면 매출 끊김""",

        2: """[수요일 - 데이터]

08:30~09:30
- 채널 점검
- 매출 확인

15:00
- 데이터 분석
- 채널 이슈 정리

16:00 미팅
- 이슈 보고
- 공유사항 확인

17:00~17:45
- 다음날 정리""",

        3: """[목요일 - 발주 준비]

08:30~09:30
- 채널 점검

09:00 미팅
- 이슈 / 성과 보고

14:00~
- 입고 일정 확인
- 재고 이관 요청

쿠팡 발주 (2~3시간)
- ID A/B 발주
- 납품금액 정리

17:00~17:45
- 다음날 정리

※ 발주 타이밍 = 매출""",

        4: """[금요일 - 마감]

08:30~09:30
- 채널 점검

10:00
- 쿠팡 발주

11:00까지
- 재고 이관 요청 완료

16:00~
- 매출 확인
- 다음주 할인 정리
- 주간 보고 작성

17:00~17:45
- 업무 정리

※ 숫자 틀리면 다음주 꼬임"""
    }

    return messages.get(weekday, None)

# ✅ 실행 루프
def run():
    while True:
        now = datetime.datetime.now()

        # 평일 08:25
        if now.weekday() < 5 and now.hour == 8 and now.minute == 25:
            send_message("[아침 루틴]\n- 채널 점검\n- 발주 확인\n- 매출 체크")

            msg = daily_message()
            if msg:
                send_message(msg)

            # 월요일이면 주차 메시지 추가
            if now.weekday() == 0:
                send_message(weekly_message())

            time.sleep(60)

        time.sleep(20)


run()

