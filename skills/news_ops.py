"""
News Operations Skill for ANU
Provides latest news headlines and updates
"""

import requests
import os
from core.skill import Skill

def get_news_headlines(category="general", country="us", num_articles=5):
    """
    Get latest news headlines
    
    Args:
        category: News category (general, business, technology, sports, entertainment, health, science)
        country: Country code (us, in, uk, ca, au)
        num_articles: Number of articles to return (1-10)
    """
    try:
        # Using NewsAPI - Free tier available
        # You can get a free API key from https://newsapi.org/
        api_key = os.environ.get("NEWS_API_KEY", "")
        
        if not api_key:
            # Fallback: Use RSS feeds without API key
            return _get_news_from_rss(category, num_articles)
        
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}&pageSize={num_articles}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") != "ok":
            return f"❌ Error fetching news: {data.get('message', 'Unknown error')}"
        
        articles = data.get("articles", [])
        
        if not articles:
            return f"📰 No news articles found for {category} category."
        
        # Format headlines
        news_text = f"📰 Here are the top {len(articles)} {category} headlines:\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            description = article.get("description", "")
            
            news_text += f"{i}. {title}\n"
            news_text += f"   Source: {source}\n"
            if description:
                news_text += f"   {description[:100]}...\n"
            news_text += "\n"
        
        return news_text.strip()
        
    except requests.exceptions.Timeout:
        return "❌ News request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching news: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def _get_news_from_rss(category="general", num_articles=5):
    """Fallback: Get news from RSS feeds without API key"""
    try:
        import feedparser
        
        # RSS feed URLs by category
        feeds = {
            "general": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
            "technology": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
            "business": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
            "sports": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
            "entertainment": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
            "health": "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US:en",
            "science": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
        }
        
        feed_url = feeds.get(category, feeds["general"])
        
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            return "📰 No news articles found. Please check your internet connection."
        
        # Format headlines
        news_text = f"📰 Here are the top {min(num_articles, len(feed.entries))} {category} headlines:\n\n"
        
        for i, entry in enumerate(feed.entries[:num_articles], 1):
            title = entry.get("title", "No title")
            source = entry.get("source", {}).get("title", "Unknown source")
            
            news_text += f"{i}. {title}\n"
            news_text += f"   Source: {source}\n\n"
        
        return news_text.strip()
        
    except ImportError:
        return "❌ feedparser library not installed. Please run: pip install feedparser"
    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"


def search_news(query, num_articles=5):
    """
    Search for specific news topics
    
    Args:
        query: Search query (e.g., "climate change", "AI technology")
        num_articles: Number of articles to return (1-10)
    """
    try:
        api_key = os.environ.get("NEWS_API_KEY", "")
        
        if not api_key:
            return "❌ News search requires NEWS_API_KEY. Get a free key from https://newsapi.org/"
        
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize={num_articles}&sortBy=publishedAt"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") != "ok":
            return f"❌ Error searching news: {data.get('message', 'Unknown error')}"
        
        articles = data.get("articles", [])
        
        if not articles:
            return f"📰 No news articles found for '{query}'."
        
        # Format results
        news_text = f"🔍 Search results for '{query}':\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            published = article.get("publishedAt", "")
            description = article.get("description", "")
            
            news_text += f"{i}. {title}\n"
            news_text += f"   Source: {source}"
            if published:
                news_text += f" | {published[:10]}"
            news_text += "\n"
            if description:
                news_text += f"   {description[:100]}...\n"
            news_text += "\n"
        
        return news_text.strip()
        
    except Exception as e:
        return f"❌ Error searching news: {str(e)}"


# Register the skill
def register():
    from core.skill import Skill
    
    class NewsSkill(Skill):
        @property
        def name(self):
            return "news_skill"
        
        def get_tools(self):
            return [
                {
                    "type": "function",
                    "function": {
                        "name": "get_news_headlines",
                        "description": "Get latest news headlines by category. Categories: general, business, technology, sports, entertainment, health, science",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "category": {
                                    "type": "string",
                                    "description": "News category: general, business, technology, sports, entertainment, health, science",
                                    "enum": ["general", "business", "technology", "sports", "entertainment", "health", "science"]
                                },
                                "country": {
                                    "type": "string",
                                    "description": "Country code: us (USA), in (India), uk (UK), ca (Canada), au (Australia)",
                                    "enum": ["us", "in", "uk", "ca", "au"]
                                },
                                "num_articles": {
                                    "type": "integer",
                                    "description": "Number of articles to return (1-10)",
                                    "default": 5
                                }
                            },
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_news",
                        "description": "Search for news articles about a specific topic",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query (e.g., 'climate change', 'AI technology')"
                                },
                                "num_articles": {
                                    "type": "integer",
                                    "description": "Number of articles to return (1-10)",
                                    "default": 5
                                }
                            },
                            "required": ["query"]
                        }
                    }
                }
            ]
        
        def get_functions(self):
            return {
                "get_news_headlines": get_news_headlines,
                "search_news": search_news
            }
    
    return NewsSkill()
