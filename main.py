from news_fetcher import NewsFetcher, get_fallback_news
from summarizer import ArticleSummarizer
from email_sender import EmailSender
from config import CATEGORIES
import schedule
import time
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DailyNewsDigestBot:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.summarizer = ArticleSummarizer()
        self.email_sender = EmailSender()
    
    def run_digest(self, use_fallback=False):
        """Run the complete news digest process"""
        logging.info("Starting daily news digest process...")
        
        try:
            # Step 1: Fetch news
            if use_fallback:
                logging.warning("Using fallback news data (API may be unavailable)")
                news_by_category = get_fallback_news()
            else:
                logging.info("Fetching news from all categories...")
                news_by_category = self.news_fetcher.fetch_all_news()
            
            # Check if we got any news
            total_articles = sum(len(articles) for articles in news_by_category.values())
            if total_articles == 0:
                logging.warning("No articles fetched from API. Trying fallback data...")
                news_by_category = get_fallback_news()
                total_articles = sum(len(articles) for articles in news_by_category.values())
                
                if total_articles == 0:
                    logging.error("No articles available from API or fallback")
                    return
            
            # Step 2: Summarize articles
            logging.info("Summarizing articles...")
            summarized_news = {}
            
            for category, articles in news_by_category.items():
                if articles:
                    summarized_articles = self.summarizer.summarize_articles(articles)
                    summarized_news[category] = summarized_articles
                    logging.info(f"Summarized {len(summarized_articles)} {category} articles")
            
            # Step 3: Send email
            logging.info("Sending email digest...")
            success = self.email_sender.create_daily_digest(summarized_news)
            
            if success:
                logging.info("Daily digest completed successfully!")
            else:
                logging.error("Failed to send daily digest")
                
        except Exception as e:
            logging.error(f"Error in digest process: {e}")
    
    def schedule_daily_digest(self, time_str: str = "08:00"):
        """Schedule the digest to run daily at specified time"""
        logging.info(f"Scheduling daily digest for {time_str}")
        schedule.every().day.at(time_str).do(self.run_digest)
        
        # Run immediately for testing
        self.run_digest()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """Main function"""
    bot = DailyNewsDigestBot()
    
    # For testing: run once immediately
    bot.run_digest()
    
    # For production: uncomment next line to schedule daily
    # bot.schedule_daily_digest("08:00")

if __name__ == "__main__":
    main()