import json
import logging
import os
import random
import time
import requests
import schedule
from dotenv import load_dotenv

# Load secrets from local .env file (or system environment in production)
load_dotenv()


# Setup logging to see output clearly in production
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

# Fetch config from environment variables (best security practice)
TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
USED_VERSES_FILE = 'used_verses.json'

AMHARIC_VERSES = [
    {
        'id': 1,
        'text': (
            'እግዚአብሔር እረኛዬ ነው፥ የሚያስፈልገኝንም አላጣውም። በለመለመ መስክ ያሳድረኛል፤ በዕረፍት'
            ' ውኃ ዘንድ ይመራኛል።'
        ),
        'ref': 'መዝሙረ ዳዊት 23:1-2',
    },
    {
        'id': 2,
        'text': 'በመከራ ቀን ጠራኝ፥ እኔም አድነሃለሁ አንተም ታከብረኛለህ።',
        'ref': 'መዝሙረ ዳዊት 50:15',
    },
    {
        'id': 3,
        'text': (
            'በፍጹም ልብህ በእግዚአብሔር ታመን፥ በራስህም ማስተዋል አትደገፍ፤ በ መንገድህ ሁሉ እርሱን'
            ' እወቅ፥ እርሱም ጎዳናህን ያቀናልህ።'
        ),
        'ref': 'መጽሐፈ ምሳሌ 3:5-6',
    },
    {
        'id': 4,
        'text': (
            'ሰላምን እተውላችኋለሁ፥ ሰላሜን እሰጣችኋለሁ፤ እኔ የምሰጣችሁ ዓለም እንደሚሰጥ አይደለም።'
            ' ልባችሁ አይደንግጥ አይፍራም።'
        ),
        'ref': 'የዮሐንስ ወንጌል 14:27',
    },
    {
        'id': 5,
        'text': (
            'ሁልጊዜ በጌታ ደስ ይበላችሁ፤ ደግሜ እላለሁ፥ ደስ ይበላችሁ! ገርነታችሁ ለሰው ሁሉ የታወቀ'
            ' ይሁን።'
        ),
        'ref': 'ወደ ፊልጵስዩስ ሰዎች 4:4-5',
    },
]


def load_used_ids():
  """Load sent verse IDs so we don't repeat them until all are sent."""
  if os.path.exists(USED_VERSES_FILE):
    with open(USED_VERSES_FILE, 'r') as f:
      try:
        return json.load(f)
      except Exception:
        return []
  return []


def save_used_ids(used_ids):
  with open(USED_VERSES_FILE, 'w') as f:
    json.dump(used_ids, f)


def send_telegram_message(text):
  """Sends text to Telegram group with retry logic."""
  url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
  payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
  try:
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code == 200:
      logging.info('Message delivered successfully.')
    else:
      logging.error(f'Failed to send message: {res.text}')
  except Exception as e:
    logging.error(f'Network error while sending message: {e}')


def send_daily_verse():
  used_ids = load_used_ids()
  available_verses = [v for v in AMHARIC_VERSES if v['id'] not in used_ids]

  # Reset list if all verses have been used once
  if not available_verses:
    used_ids = []
    available_verses = AMHARIC_VERSES

  verse = random.choice(available_verses)
  used_ids.append(verse['id'])
  save_used_ids(used_ids)

  msg = (
      "📖 **የዕለቱ መጽሐፍ ቅዱስ ጥቅስ**\n\n"
      f'"{verse["text"]}"\n\n'
      f'📍 *{verse["ref"]}*\n\n'
      "መልካም እና የተባረከ ቀን ይሁንልን! ☦️"
  )
  send_telegram_message(msg)


def send_morning_prayer_reminder():
  msg = (
      "🔔 **የነግህ ጸሎት ማስታወሻ**\n\n"
      "የግቢ ጉባኤያችን አባላት፡ የቀኑን ተግባራችንን ከመጀመራችን በፊት የነግህ ጸሎታችንን እናድርስ።\n\n"
      ' "በማለዳ ጸሎቴን ወደ አንተ አቀርባለሁ..." (መዝ 5:3) 🙏'
  )
  send_telegram_message(msg)


def send_evening_prayer_reminder():
  msg = (
      "🌙 **የሠርክ (የምሽት) ጸሎት ማስታወሻ**\n\n"
      "ዕለቱን በሰላም ላስፈጸመን እግዚአብሔር ምስጋና ይሁን። ወደ እረፍት ከመሄዳችን በፊት የምሽት ጸሎታችንን"
      " እንጸልይ። 🙏✨"
  )
  send_telegram_message(msg)


# --- SCHEDULE (Times in 24-hour format) ---
schedule.every().day.at("06:00").do(send_morning_prayer_reminder)
schedule.every().day.at("06:30").do(send_daily_verse)
schedule.every().day.at("21:00").do(send_evening_prayer_reminder)

if __name__ == "__main__":
  logging.info("☦️ Gibi Gebeya Bot Started in Production Mode...")
  while True:
    schedule.run_pending()
    time.sleep(30)  # Sleep 30s to preserve CPU resources