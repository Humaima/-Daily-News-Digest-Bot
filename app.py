import streamlit as st
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Daily News Digest Bot",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .news-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class NewsDigestApp:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
    
    def fetch_news(self, category='technology', max_results=5):
        """Fetch news from NewsData.io"""
        if not self.api_key or self.api_key.startswith('your_'):
            return None, "❌ Please configure your NewsData.io API key in the .env file"
        
        try:
            url = "https://newsdata.io/api/1/news"
            params = {
                'apikey': self.api_key,
                'category': category,
                'language': 'en',
                'size': max_results
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('results', []), None
                else:
                    return None, data.get('message', 'Unknown API error')
            else:
                return None, f"HTTP Error {response.status_code}"
                
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def simple_summarize(self, text, max_sentences=2):
        """Simple text summarization"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        if len(sentences) > max_sentences:
            return '. '.join(sentences[:max_sentences]) + '.'
        return text[:200] + '...' if len(text) > 200 else text
    
    def send_email(self, subject, body, recipient_email):
        """Send email with news digest"""
        if not all([self.email_user, self.email_password]):
            return False, "Email credentials not configured"
        
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = recipient_email
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, recipient_email, msg.as_string())
            
            return True, "Email sent successfully!"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def run_digest(self, categories, recipient_email, articles_per_category=3):
        """Run complete news digest"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_articles = {}
        
        # Fetch news for each category
        for i, category in enumerate(categories):
            status_text.text(f"📡 Fetching {category} news...")
            articles, error = self.fetch_news(category, articles_per_category)
            
            if error:
                st.warning(f"Could not fetch {category} news: {error}")
                # Add fallback article
                all_articles[category] = [{
                    'title': f'{category.capitalize()} News Update',
                    'description': f'Latest developments in {category}',
                    'content': f'Stay tuned for the latest {category} news updates.',
                    'source': 'News Digest Bot',
                    'url': ''
                }]
            else:
                all_articles[category] = articles or []
            
            progress_bar.progress((i + 1) / len(categories) * 0.4)
        
        # Process and summarize articles
        status_text.text("📝 Summarizing articles...")
        processed_articles = {}
        
        for category, articles in all_articles.items():
            summarized_articles = []
            for article in articles:
                summary = self.simple_summarize(
                    f"{article.get('title', '')}. {article.get('description', '')}. {article.get('content', '')}"
                )
                article['summary'] = summary
                summarized_articles.append(article)
            processed_articles[category] = summarized_articles
        
        progress_bar.progress(0.8)
        
        # Create email content
        status_text.text("✉️ Preparing email...")
        date_str = datetime.now().strftime("%B %d, %Y")
        subject = f"📰 Daily News Digest - {date_str}"
        
        body = f"Daily News Digest - {date_str}\n"
        body += "=" * 50 + "\n\n"
        
        for category, articles in processed_articles.items():
            body += f"🎯 {category.upper()} NEWS:\n"
            body += "-" * 30 + "\n"
            
            for i, article in enumerate(articles, 1):
                body += f"{i}. {article.get('title', 'No title')}\n"
                body += f"   📍 Source: {article.get('source_id', article.get('source', 'Unknown'))}\n"
                body += f"   📝 {article.get('summary', article.get('description', ''))}\n"
                if article.get('url'):
                    body += f"   🔗 Read more: {article.get('url')}\n"
                body += "\n"
        
        body += "=" * 50 + "\n"
        body += "Sent by your Daily News Digest Bot 📰"
        
        # Send email
        success, message = self.send_email(subject, body, recipient_email)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Complete!")
        
        return success, message, processed_articles

def main():
    # Initialize app
    app = NewsDigestApp()
    
    # Header
    st.markdown('<h1 class="main-header">📰 Daily News Digest Bot</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("News Sources")
        categories = st.multiselect(
            "Select categories:",
            ["business", "technology", "science", "health", "entertainment", "sports"],
            default=["technology", "science", "business"]
        )
        
        articles_per_category = st.slider("Articles per category:", 1, 10, 3)
        
        st.subheader("Email Settings")
        recipient_email = st.text_input("Recipient Email:", os.getenv('RECIPIENT_EMAIL', ''))
        
        st.subheader("API Status")
        if app.api_key and not app.api_key.startswith('your_'):
            st.success("✅ NewsData.io API: Configured")
        else:
            st.error("❌ NewsData.io API: Not configured")
            
        if app.email_user and app.email_password:
            st.success("✅ Email Service: Configured")
        else:
            st.warning("⚠️ Email Service: Not configured")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Quick Start")
        st.write("""
        1. Configure your API keys in the `.env` file
        2. Select news categories on the left
        3. Enter recipient email address
        4. Click 'Run Daily Digest' to send news
        """)
        
        if st.button("🎯 Run Daily Digest", type="primary"):
            if not categories:
                st.error("Please select at least one news category")
            elif not recipient_email:
                st.error("Please enter a recipient email address")
            else:
                success, message, articles = app.run_digest(categories, recipient_email, articles_per_category)
                
                if success:
                    st.success(message)
                    
                    # Show preview
                    st.subheader("📊 Digest Preview")
                    for category, category_articles in articles.items():
                        with st.expander(f"📰 {category.upper()} ({len(category_articles)} articles)"):
                            for article in category_articles:
                                st.markdown(f"""
                                <div class="news-card">
                                    <h4>{article.get('title', 'No title')}</h4>
                                    <p>{article.get('summary', article.get('description', ''))}</p>
                                    <small>Source: {article.get('source_id', article.get('source', 'Unknown'))}</small>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.error(message)
    
    with col2:
        st.subheader("📋 Setup Guide")
        
        with st.expander("🔧 API Configuration"):
            st.write("""
            **1. NewsData.io API:**
            - Get free key: [newsdata.io/pricing](https://newsdata.io/pricing)
            - Add to `.env`: `NEWSDATA_API_KEY=your_key`
            
            **2. Gmail Setup:**
            - Enable 2FA on Gmail
            - Generate app password
            - Add to `.env`: 
              ```
              EMAIL_USER=your_email@gmail.com
              EMAIL_PASSWORD=your_app_password
              ```
            """)
        
        with st.expander("📁 .env File Example"):
            st.code("""
# NewsData.io API
NEWS_API_KEY=your_actual_api_key_here

# Gmail Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient@email.com
            """)
        
        with st.expander("🛠️ Troubleshooting"):
            st.write("""
            **Common Issues:**
            - 401 Error: Check API key in .env file
            - Email errors: Verify Gmail app password
            - No articles: API might be rate-limited
            
            **Fallback Mode:**
            App will use sample data if API fails
            """)

if __name__ == "__main__":
    main()