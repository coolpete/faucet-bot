import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
import os

# Gmail email alert config
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

# Faucets list - extend as needed
faucet_list = [
    {"name": "FireFaucet", "url": "https://firefaucet.win", "requires_captcha": True},
    {"name": "DutchyCorp", "url": "https://autofaucet.dutchycorp.space", "requires_captcha": False},
    {"name": "Cointiply", "url": "https://cointiply.com", "requires_captcha": True},
    {"name": "AllCoins", "url": "https://allcoins.pw", "requires_captcha": False}
]

wallet_address = "0x528Be1ffF7703e60b12733B31f1c1B4947082D73"

def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = ALERT_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def claim_faucet(faucet):
    if faucet["requires_captcha"]:
        alert_subject = f"Alert: CAPTCHA detected on {faucet['name']}"
        alert_msg = f"Manual claim required for {faucet['name']} ({faucet['url']})."
        send_email_alert(alert_subject, alert_msg)
        return {"status": "skipped", "reason": "CAPTCHA detected"}
    else:
        # Simulate claim success
        return {"status": "claimed", "amount": "0.00001 ETH"}

def run_bot():
    claim_log = []
    for faucet in faucet_list:
        result = claim_faucet(faucet)
        claim_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "faucet": faucet["name"],
            "url": faucet["url"],
            "status": result["status"],
            "reason_or_amount": result.get("reason", result.get("amount", ""))
        })
    # Save log to file
    with open("claim_log.json", "w") as f:
        json.dump(claim_log, f, indent=2)
    print("Run completed. Log saved.")

if __name__ == "__main__":
    run_bot()
