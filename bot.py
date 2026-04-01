import requests
import os
from datetime import datetime, date
from zoneinfo import ZoneInfo

import os
TOKEN = os.getenv("8513262392:AAGlDEyw-Vkmcoj0CjzZzDo2oYM9-M2p9GA")
CHAT_ID = os.getenv("8250645779")


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}

    res = requests.post(url, data=data)

    print("========== TELEGRAM DEBUG ==========")
    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)
    print("====================================")


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


def get_week_of_month():
    today = date.today()
    first_day = today.replace(day=1)
    return (today.day + first_day.weekday()) // 7 + 1


def is_last_workday():
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    try:
        next_day = today.replace(day=today.day + 1)
    except:
        return today.weekday() < 5

    if next_day.month != today.month:
        return today.weekday() < 5

    return False


def common_message():
    return (
        "[공통 업무]\n"
        "- 운영채널 가격/이슈/매출 점검\n"
        "- 쿠팡 서플라이허브 발주서 확인\n"
        "- 예상 납품 금액 정리"
    )


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

    print("현재 한국 시간:", now)

    if now.weekday() >= 5:
        print("주말이라 실행 안함")
        return

    if already_sent_today():
        print("이미 오늘 보냄")
        return

    send_message(common_message())
    send_message(daily_message(now.weekday()))

    if now.weekday() == 0:
        send_message(weekly_message())

    if is_last_workday():
        send_message("[월말 업무]\n- 월말 마감 체크")

    mark_sent()

print("현재 TOKEN:", TOKEN)
run()
