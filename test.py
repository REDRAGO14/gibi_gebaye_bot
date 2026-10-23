import os
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def test_send():
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  test_message = (
      "☦️ **BITS ቃለ ሕይወት Bot (BITS Qale Hiywot Bot)**\n\n"
      "ሰላም ለሁላችሁ ይሁን! ቦቱ በትክክል ሥራ ጀምሯል።\n\n"
      ' *"ቃሉ ለእግሬ መብራት፥ ለጎዳናዬም ብርሃን ነው።"* — መዝሙረ ዳዊት 119:105'
  )

  payload = {"chat_id": CHAT_ID, "text": test_message, "parse_mode": "Markdown"}

  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print("✅ Success! Test message delivered to your group chat.")
  else:
    print(f"❌ Failed to send message. Error: {response.text}")


if __name__ == "__main__":
  test_send()