import requests
from datetime import datetime, date
from zoneinfo import ZoneInfo

TOKEN = "8513262392:AAEH5OkiGB4cFUR3lLRb01admHVz9Jrb0yc"
CHAT_ID = "8250645779"
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)
# ✅ 중복 방지 (하루 1번)
def already_sent_today():
    today = date.today()
    try:
        with open("sent_log.txt", "r") as f:
            return f.read() == str(today)
    except:
        return False


def mark_sent():
    today = date.today()
    with open("sent_log.txt", "w") as f:
        f.write(str(today))


# ✅ 주차 계산
def get_week_of_month():
    today = date.today()
    first_day = today.replace(day=1)
    return (today.day + first_day.weekday()) // 7 + 1


# ✅ 월말 평일 체크
def is_last_workday():
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    next_day = today.replace(day=today.day + 1)

    # 다음날이 다른 달이면 오늘이 월말
    if next_day.month != today.month:
        return today.weekday() < 5

    return False


# ✅ 공통 메시지
def common_message():
    return (
        "[공통 업무]\n"
        "- 운영채널 가격/이슈/매출 점검\n"
        "- 쿠팡 서플라이허브 발주서 확인\n"
        "- 예상 납품 금액 정리"
    )


# ✅ 요일별 메시지
def daily_message(weekday):
    messages = {
        0: "[월요일]\n기본 운영 집중",

        1: "[화요일]\n"
           "10:30 회의준비 (기영이팀)\n"
           "- 리오더/부족수량\n"
           "- 입고일정 확인\n"
           "- 영업 요청사항\n\n"
           "11:00 회의\n"
           "- 급한 품번 공유\n\n"
           "14:00 AX TFT",

        2: "[수요일]\n"
           "15:00 회의준비 (영업팀)\n"
           "- 데이터 분석\n"
           "- 채널 이슈\n\n"
           "16:00 회의\n"
           "- 이슈 보고\n"
           "- 공유사항",

        3: "[목요일]\n"
           "09:00 유통부 회의\n"
           "- 채널 이슈/성과/지시사항\n\n"
           "14:00~\n"
           "[쿠팡 발주 전]\n"
           "- 입고일정 확인\n"
           "- 이관 시트 작성\n\n"
           "[쿠팡 발주]",

        4: "[금요일]\n"
           "11:00 이관 요청 시트\n\n"
           "14:00 쿠팡 발주\n\n"
           "[금주 마감]\n"
           "- 일정 정리\n"
           "- 다음주 계획\n"
           "- 주간 보고"
    }

    return messages.get(weekday, "")
# ✅ 월요일 주간 메시지
def weekly_message():
    week = get_week_of_month()

    messages = {
        1: "[1주차]\n- 반출예상 수량\n- 대시보드\n- 개인경비",
        2: "[2주차]\n- 부족 수량 공유",
        3: "[3주차]\n- 영업계획\n- 매입 마감",
        4: "[4주차]\n- 사전 발주 계산",
        5: "[5주차]\n- 추가 점검"
    }

    return messages.get(week, "")


def run():
    now = datetime.now(ZoneInfo("Asia/Seoul"))

    # ✅ 평일만
    if now.weekday() >= 5:
        return

    # ✅ 원하는 시간 (예: 08:20)
    if not (now.hour == 8 and now.minute == 20):
        return

    # ✅ 하루 1번 제한
    if already_sent_today():
        return

    # 1️⃣ 공통
    send_message(common_message())

    # 2️⃣ 요일별
    send_message(daily_message(now.weekday()))

    # 3️⃣ 월요일 + 주차
    if now.weekday() == 0:
        send_message(weekly_message())

    # 4️⃣ 월말
    if is_last_workday():
        send_message("[월말 업무]\n- 월말 마감 체크")

    mark_sent()


run()
