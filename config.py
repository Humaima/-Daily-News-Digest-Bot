import os
from dotenv import load_dotenv

load_dotenv()

# NewsData.io API Configuration
NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')
NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Email Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# News Categories to fetch
CATEGORIES = ['business', 'technology', 'science', 'health', 'entertainment']

# Number of articles per category
ARTICLES_PER_CATEGORY = 3