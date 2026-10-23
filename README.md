# ☦️ Orthodox Gibi Gebeya Telegram Bot (የግቢ ጉባኤ ቦት)

An automated Telegram bot created for Ethiopian Orthodox Tewahedo Church (EOTC) **Gibi Gebeya (ግቢ ጉባኤ)** student fellowship groups. The bot helps keep members spiritually connected through automated daily Amharic Bible verses and scheduled prayer reminders.

---

## 🌟 Key Features

- 📖 **Daily Amharic Bible Verses (የዕለቱ መጽሐፍ ቅዱስ ጥቅስ):** Automatically selects and formats daily Scripture verses in Amharic every morning.
- 🔄 **Smart Verse Rotation:** Tracks previously sent verses to avoid immediate repetition until all verses in the collection have been shared.
- 🔔 **Prayer Reminders (የጸሎት ማስታወሻ):** Automatically posts daily prayer notifications for Morning (ነግህ) and Evening (ሠርክ) prayers.
- 🔐 **Secure Configuration:** Uses environment variables to keep Telegram API tokens and Group Chat IDs safe.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.x
- **Libraries:**
  - [`requests`](https://pypi.org/project/requests/) – Handles Telegram Bot API calls.
  - [`schedule`](https://pypi.org/project/schedule/) – Manages accurate time-based job execution.
  - [`python-dotenv`](https://pypi.org/project/python-dotenv/) – Manages environment variables locally.

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.8 or higher installed on your computer.
- A Telegram Bot token obtained from [@BotFather](https://t.me/BotFather).
- A Telegram Group Chat ID where the bot will post.

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/gibi-gebeya-bot.git](https://github.com/your-username/gibi-gebeya-bot.git)
   cd gibi-gebeya-bot