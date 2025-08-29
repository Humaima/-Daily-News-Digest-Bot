# 📰 Daily News Digest Bot

A powerful and customizable automated system that fetches news articles, summarizes them using AI, and delivers personalized email digests. Perfect for staying informed with your preferred news categories delivered directly to your inbox.

<img width="1358" height="692" alt="image" src="https://github.com/user-attachments/assets/1cd38d73-84eb-4245-926e-4078b2d9eaf8" />

<img width="1366" height="647" alt="image" src="https://github.com/user-attachments/assets/5df70dec-7bae-4ef3-bacf-eaab3219a045" />

<img width="746" height="602" alt="image" src="https://github.com/user-attachments/assets/6965de99-fcdc-4dcc-80a9-a5eb96f37d45" />


---

## ✨ Features

- 📡 **Multi-Source News Aggregation:** Fetch news from **NewsData.io API**
- 🤖 **AI-Powered Summarization:** Uses **Google Gemini** for intelligent article summarization
- 📧 **Automated Email Delivery:** Sends beautifully formatted daily digests
- 🎨 **Beautiful Web Interface:** Streamlit-based dashboard for easy configuration
- ⚙️ **Customizable Categories:** Pick business, technology, science, health, entertainment, and more
- 🔧 **Fallback System:** Graceful degradation when APIs are unavailable

---

---

## 🚀 Quick Start

### Prerequisites
- Python **3.8+**
- Gmail account (for sending emails)
- **NewsData.io** API key (free tier available)
- **Google Gemini** API key (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/daily-news-digest-bot.git
cd daily-news-digest-bot

# Create virtual environment
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Then edit .env with your credentials
```

### ⚙️ Configuration

Edit the .env file with your credentials:

```bash
# NewsData.io API Key (get from: https://newsdata.io/pricing)
NEWSDATA_API_KEY=your_actual_api_key_here

# Gmail Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient@email.com

# Gemini API (optional - get from: https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_optional
```

### Getting API Keys (no fluff, just steps)
## NewsData.io API Key

- Visit NewsData.io Pricing
- Sign up for a free account
- Get your API key from the dashboard

## Gmail App Password

- Enable 2FA on your Google account
- Generate an App password for “Mail”
- Use the 16-character password (not your login password)

## Gemini API Key 

- Visit Google AI Studio
- Create an API key for Gemini

### 🎯 Usage

Command Line Interface:

```bash
# Run the daily digest
python main.py

# Run with specific categories and article count
python main.py --categories technology science --articles 5
```

### Web Interface (Recommended)

The web interface provides:

- Visual category selection
- Real-time preview of articles
- Email configuration
- API status monitoring
- One-click digest generation

### 🛡️ Security Notes (straight talk)

- Use a Gmail App Password, never your real password.
- Don’t commit .env to git. Add it to .gitignore.
- Rate limits are real. Handle API quotas and add retries/backoff.
- Log minimally; avoid logging secrets or full article payloads.

### 🤝 Contributing

PRs welcome. Keep changes minimal, focused, and tested. Follow conventional commits if you can.

### 📄 License

MIT — do what you want, don’t blame the authors if you break it.
