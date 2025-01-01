import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from config import *

WINNING_NUMBERS = ["1908", "6908"]

def fetch_lottery_results():
    url = "https://www.molottery.com/pick4"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        midday_title = soup.find("div", class_="game-single-calendar__title", text="Midday")
        midday_body = midday_title.find_next_sibling("div", class_="game-single-calendar__body")
        numbers = midday_body.find_all("div", class_="game-single-calendar__num")
        result = "".join(num.text.strip() for num in numbers)
        print(f"Today's Midday Results: {result}")
        return result
    else:
        raise Exception("Failed to fetch lottery results.")


def send_email_notification(result):
    win_or_lose = "WINNER" if result in WINNING_NUMBERS else "Not today :("
    msg_content = f"""
    Today's Missouri Pick 4 Midday Results: {result}.
    Your numbers: {str(WINNING_NUMBERS[0])} & {str(WINNING_NUMBERS[1])}
    {"YOU WON!" if result in WINNING_NUMBERS else "Not today :("}
    """
    title_content = f"Daily Lottery Result: {win_or_lose}"
    
    msg = MIMEText(msg_content)
    msg["Subject"] = title_content
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Email notification sent!")


def main():
    try:
        results = fetch_lottery_results()
        send_email_notification(results)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
