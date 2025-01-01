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

def check_results(results):
    return any(number in results for number in WINNING_NUMBERS)

def send_email_notification(results):
    msg_content = f"""
    Your number matched the Pick 4 Midday Results: {results}.

    Your numbers: {WINNING_NUMBERS}
    """
    msg = MIMEText(msg_content)
    msg["Subject"] = f"Daily Lottery Result: {results}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Email notification sent!")

# Main logic
def main():
    try:
        results = fetch_lottery_results()
        send_email_notification(results)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()