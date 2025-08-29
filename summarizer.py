import google.generativeai as genai
from config import GEMINI_API_KEY
from typing import List, Dict
import re

class ArticleSummarizer:
    def __init__(self):
        self.gemini_api_key = GEMINI_API_KEY
        self.setup_gemini()
    
    def setup_gemini(self):
        """Initialize Gemini AI with correct API version"""
        if self.gemini_api_key and not self.gemini_api_key.startswith('your_'):
            try:
                # Configure with correct API version
                genai.configure(
                    api_key=self.gemini_api_key,
                    transport='rest'  # Use REST instead of grpc
                )
                
                # List available models to find the correct one
                try:
                    models = genai.list_models()
                    available_models = [model.name for model in models]
                    print(f"✅ Available models: {available_models}")
                    
                    # Use gemini-1.0-pro if available, otherwise try alternatives
                    if 'models/gemini-pro' in available_models:
                        self.model = genai.GenerativeModel('gemini-pro')
                    elif 'models/gemini-1.0-pro' in available_models:
                        self.model = genai.GenerativeModel('gemini-1.0-pro')
                    else:
                        print("❌ No compatible Gemini models found")
                        self.gemini_available = False
                        return
                        
                    self.gemini_available = True
                    print("✅ Gemini AI initialized successfully")
                    
                except Exception as e:
                    print(f"❌ Error listing models: {e}")
                    self.gemini_available = False
                    
            except Exception as e:
                print(f"❌ Gemini setup failed: {e}")
                self.gemini_available = False
        else:
            print("ℹ️ Gemini API key not found or is placeholder")
            self.gemini_available = False
    
    def summarize_article(self, article: Dict) -> Dict:
        """Summarize a single article"""
        content_to_summarize = f"{article['title']}. {article.get('description', '')}. {article.get('content', '')}"
        
        if self.gemini_available:
            summary = self._summarize_with_gemini(content_to_summarize)
        else:
            summary = self._simple_summarize(content_to_summarize)
        
        article['summary'] = summary
        return article
    
    def _summarize_with_gemini(self, text: str) -> str:
        """Summarize using Gemini AI"""
        try:
            # Clean and truncate text if too long
            clean_text = self._clean_text(text[:4000])  # Limit to Gemini's input size
            
            prompt = f"""
            Create a concise 2-3 sentence summary of this news article:
            
            {clean_text}
            
            Summary:
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"❌ Gemini summarization error: {e}")
            return self._simple_summarize(text)
    
    def _simple_summarize(self, text: str, max_sentences: int = 2) -> str:
        """Simple summarization without external APIs"""
        clean_text = self._clean_text(text)
        sentences = re.split(r'[.!?]+', clean_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > max_sentences:
            return '. '.join(sentences[:max_sentences]) + '.'
        return clean_text[:150] + '...' if len(clean_text) > 150 else clean_text
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        text = ' '.join(text.split())
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """Summarize multiple articles"""
        summarized_articles = []
        
        for i, article in enumerate(articles):
            print(f"📝 Summarizing article {i+1}/{len(articles)}...")
            summarized = self.summarize_article(article)
            summarized_articles.append(summarized)
        
        return summarized_articles