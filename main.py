import json
import logging
import os
import random
import threading
import time
from dotenv import load_dotenv
from flask import Flask
import requests
import schedule

# Load environment variables
load_dotenv()

# --- FLASK WEBSERVER FOR RENDER ---
app = Flask(__name__)


@app.route("/")
def home():
  return "☦️ BITS ቃለ ሕይወት Bot is active and running!"


def run_webserver():
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)


# --- BOT CONFIGURATION ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
USED_VERSES_FILE = "used_verses.json"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

AMHARIC_VERSES = [
    {
        "id": 1,
        "text": (
            "እግዚአብሔር እረኛዬ ነው፥ የሚያስፈልገኝንም አላጣውም። በለመለመ መስክ ያሳድረኛል፤ በዕረፍት"
            " ውኃ ዘንድ ይመራኛል።"
        ),
        "ref": "መዝሙረ ዳዊት 23:1-2",
    },
    {
        "id": 2,
        "text": "በመከራ ቀን ጠራኝ፥ እኔም አድነሃለሁ አንተም ታከብረኛለህ።",
        "ref": "መዝሙረ ዳዊት 50:15",
    },
    {
        "id": 3,
        "text": (
            "በፍጹም ልብህ በእግዚአብሔር ታመን፥ በራስህም ማስተዋል አትደገፍ፤ በ መንገድህ ሁሉ እርሱን"
            " እወቅ፥ እርሱም ጎዳናህን ያቀናልህ።"
        ),
        "ref": "መጽሐፈ ምሳሌ 3:5-6",
    },
    {
        "id": 4,
        "text": (
            "ሰላምን እተውላችኋለሁ፥ ሰላሜን እሰጣችኋለሁ፤ እኔ የምሰጣችሁ ዓለም እንደሚሰጥ አይደለም።"
            " ልባችሁ አይደንግጥ አይፍራም።"
        ),
        "ref": "የዮሐንስ ወንጌል 14:27",
    },
]


def load_used_ids():
  if os.path.exists(USED_VERSES_FILE):
    with open(USED_VERSES_FILE, "r") as f:
      try:
        return json.load(f)
      except Exception:
        return []
  return []


def save_used_ids(used_ids):
  with open(USED_VERSES_FILE, "w") as f:
    json.dump(used_ids, f)


def send_telegram_message(text):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
  try:
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
      logging.info("Message sent successfully!")
    else:
      logging.error(f"Failed to send: {res.text}")
  except Exception as e:
    logging.error(f"Error: {e}")


def send_morning_prayer_reminder():
  msg = (
      "🔔 **የነግህ ጸሎት ማስታወሻ**\n\n"
      "የግቢ ጉባኤያችን አባላት፡ የቀኑን ተግባራችንን ከመጀመራችን በፊት የነግህ ጸሎታችንን እናድርስ።\n\n"
      ' "በማለዳ ጸሎቴን ወደ አንተ አቀርባለሁ..." (መዝ 5:3) 🙏'
  )
  send_telegram_message(msg)


def send_daily_verse():
  used_ids = load_used_ids()
  available = [v for v in AMHARIC_VERSES if v["id"] not in used_ids]
  if not available:
    used_ids = []
    available = AMHARIC_VERSES

  verse = random.choice(available)
  used_ids.append(verse["id"])
  save_used_ids(used_ids)

  msg = (
      "📖 **የዕለቱ መጽሐፍ ቅዱስ ጥቅስ**\n\n"
      f'"{verse["text"]}"\n\n'
      f'📍 *{verse["ref"]}*\n\n'
      "መልካም እና የተባረከ ቀን ይሁንልን! ☦️"
  )
  send_telegram_message(msg)


def send_evening_prayer_reminder():
  msg = (
      "🌙 **የሠርክ (የምሽት) ጸሎት ማስታወሻ**\n\n"
      "ዕለቱን በሰላም ላስፈጸመን እግዚአብሔር ምስጋና ይሁን። ወደ እረፍት ከመሄዳችን በፊት የምሽት ጸሎታችንን"
      " እንጸልይ። 🙏✨"
  )
  send_telegram_message(msg)


# --- SCHEDULE (Times in UTC - Ethiopia is UTC+3) ---
# 6:00 AM EAT  -> 03:00 UTC
# 6:30 AM EAT  -> 03:30 UTC
# 9:00 PM EAT  -> 18:00 UTC
schedule.every().day.at("03:00").do(send_morning_prayer_reminder)
schedule.every().day.at("03:30").do(send_daily_verse)
schedule.every().day.at("18:00").do(send_evening_prayer_reminder)


def run_scheduler():
  while True:
    schedule.run_pending()
    time.sleep(30)


if __name__ == "__main__":
  logging.info("☦️ BITS Qale Hiywot Bot Starting...")

  # Start the schedule loop on a background thread
  t = threading.Thread(target=run_scheduler)
  t.daemon = True
  t.start()

  # Start the webserver
  run_webserver()