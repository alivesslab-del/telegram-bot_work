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


def weekly_message():
    week = get_week_of_month()

    if week == 1:
        return "[이번주 핵심: 세팅]\n- 인스탁 수량 확인\n- 시트 초기화\n- 메이커스 정산 + ERP\n- 익월 상품 제안"

    elif week == 2:
        return "[이번주 핵심: 기획]\n- 프로모션 초안\n- 매출 체크\n- MD 커뮤니케이션"

    elif week == 3:
        return "[이번주 핵심: 확정]\n- 프로모션 확정\n- 리오더 준비\n- 콘텐츠 요청"

    else:
        return "[이번주 핵심: 마감]\n- 반출 금액 계산\n- 발주 준비\n- 매입 체크"


def daily_message():
    weekday = datetime.datetime.now().weekday()

    messages = {
        0: """[월요일]

08:30~09:30
- 채널 점검
- 발주 확인
- 매출 체크

오전/오후
- 방향 설정
- 일정 체크

17:00~17:45
- 다음날 정리""",

        1: """[화요일 - 리오더]

11:30 준비
- 재고 점검
- 입고 일정

14:00 미팅
- 부족 수량 공유""",

        2: """[수요일 - 데이터]

15:00
- 데이터 분석
- 이슈 정리

16:00 미팅""",

        3: """[목요일 - 발주]

14:00~
- 입고 확인
- 이관 요청

쿠팡 발주 진행""",

        4: """[금요일 - 마감]

10:00 발주

16:00~
- 매출 확인
- 주간 보고"""
    }

    return messages.get(weekday, None)


def run():
    now = datetime.datetime.now()

    if now.weekday() < 5:
        send_message("🕘 아침 루틴\n- 채널 점검\n- 발주 확인\n- 매출 체크")

        msg = daily_message()
        if msg:
            send_message(msg)

        if now.weekday() == 0:
            send_message(weekly_message())


run()
