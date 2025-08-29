import requests
from config import NEWSDATA_API_KEY, NEWSDATA_BASE_URL, CATEGORIES, ARTICLES_PER_CATEGORY
from typing import List, Dict
import json

class NewsFetcher:
    def __init__(self):
        self.api_key = NEWSDATA_API_KEY
        self.base_url = NEWSDATA_BASE_URL
        
        if not self.api_key or self.api_key.startswith('your_'):
            print("❌ WARNING: Invalid or missing NewsData.io API key")
            print("💡 Get free key from: https://newsdata.io/pricing")
    
    def fetch_news_by_category(self, category: str, max_results: int = 5) -> List[Dict]:
        """Fetch news articles for a specific category"""
        # Check if API key is valid
        if not self.api_key or self.api_key.startswith('your_'):
            print(f"❌ Skipping {category} - Invalid API key")
            return []
        
        try:
            params = {
                'apikey': self.api_key,
                'category': category,
                'language': 'en',
                'size': max_results
            }
            
            print(f"   🔗 Requesting {category} news...")
            response = requests.get(self.base_url, params=params, timeout=30)
            
            # Check for specific HTTP errors
            if response.status_code == 401:
                print(f"   ❌ 401 Unauthorized for {category} - Check API key")
                return []
            elif response.status_code == 429:
                print(f"   ⚠️  Rate limit exceeded for {category}")
                return []
            elif response.status_code != 200:
                print(f"   ❌ HTTP {response.status_code} for {category}")
                return []
                
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'success':
                articles = data.get('results', [])
                print(f"   ✅ Found {len(articles)} {category} articles")
                return self._process_articles(articles)
            else:
                error_msg = data.get('message', 'Unknown error')
                print(f"   ❌ API error for {category}: {error_msg}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network error for {category}: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON error for {category}: {e}")
            return []
    
    def _process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Process and clean article data"""
        processed_articles = []
        
        for article in articles:
            # Skip articles without title
            if not article.get('title'):
                continue
                
            processed_article = {
                'title': article.get('title', '').strip(),
                'description': article.get('description', '').strip(),
                'content': article.get('content', '').strip(),
                'source': article.get('source_id', 'Unknown'),
                'url': article.get('link', ''),
                'published_at': article.get('pubDate', ''),
                'category': article.get('category', ['general'])[0] if article.get('category') else 'general'
            }
            
            # Limit content length for summarization
            if len(processed_article['content']) > 1000:
                processed_article['content'] = processed_article['content'][:1000] + '...'
            
            processed_articles.append(processed_article)
        
        return processed_articles
    
    def fetch_all_news(self) -> Dict[str, List[Dict]]:
        """Fetch news for all categories"""
        all_news = {}
        
        print("📡 Fetching news from categories:", ', '.join(CATEGORIES))
        
        for category in CATEGORIES:
            print(f"\n🎯 {category.capitalize()} News:")
            articles = self.fetch_news_by_category(category, ARTICLES_PER_CATEGORY)
            all_news[category] = articles
        
        total_articles = sum(len(articles) for articles in all_news.values())
        print(f"\n📊 Total articles fetched: {total_articles}")
        
        return all_news

# Fallback news data for testing
def get_fallback_news():
    """Provide fallback news data when API fails"""
    return {
        'technology': [
            {
                'title': 'AI Development Advances Rapidly',
                'description': 'Researchers make breakthrough in artificial intelligence capabilities',
                'content': 'Scientists have developed new algorithms that significantly improve machine learning performance across various applications.',
                'source': 'TechNews',
                'url': '',
                'published_at': '2024-01-15',
                'category': 'technology'
            }
        ],
        'science': [
            {
                'title': 'New Space Telescope Launched',
                'description': 'Advanced telescope will explore distant galaxies',
                'content': 'The new orbital telescope promises to revolutionize our understanding of the universe with unprecedented resolution.',
                'source': 'ScienceDaily',
                'url': '',
                'published_at': '2024-01-15',
                'category': 'science'
            }
        ]
    }