import requests
from datetime import datetime
import time
from newspaper import Article, Config
import os

# NewsAPI Configuration
NEWS_API_KEY = "fea213eb8b1d4b93b2b968c9f43bdb1d"
PAGE_SIZE = 10  # Reduced for better testing

def fetch_news():
    """Fetch news with multiple fallback endpoints"""
    endpoints = [
        f"https://newsapi.org/v2/top-headlines?country=in&pageSize={PAGE_SIZE}&apiKey={NEWS_API_KEY}",
        f"https://newsapi.org/v2/everything?q=India&language=en&pageSize={PAGE_SIZE}&apiKey={NEWS_API_KEY}",
        f"https://newsapi.org/v2/top-headlines?sources=the-hindu,bbc-news&pageSize={PAGE_SIZE}&apiKey={NEWS_API_KEY}"
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=20)
            data = response.json()
            if data["status"] == "ok" and data["totalResults"] > 0:
                print(f"✅ Found {data['totalResults']} articles via {url.split('?')[0]}")
                return data["articles"]
        except Exception as e:
            print(f"⚠️ Failed with {url}: {str(e)}")
        time.sleep(2)
    return []

def extract_full_article(url):
    """Extract complete article content using newspaper3k"""
    try:
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        config.request_timeout = 15
        
        article = Article(url, config=config)
        article.download()
        article.parse()
        
        if len(article.text) > 300:  # Minimum content length
            return {
                'title': article.title,
                'content': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date
            }
    except Exception as e:
        print(f"❌ Extraction failed for {url}: {str(e)}")
    return None

def save_full_articles(articles):
    """Save complete articles with proper formatting"""
    if not articles:
        print("❌ No articles to save")
        return
    
    filename = f"full_news_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📰 COMPLETE NEWS DIGEST ({datetime.now().strftime('%d %b %Y %H:%M')})\n\n")
        f.write(f"📋 Total Articles: {len(articles)}\n\n")
        f.write("="*100 + "\n\n")
        
        for idx, article in enumerate(articles, 1):
            f.write(f"🎯 ARTICLE {idx}: {article['title']}\n")
            f.write(f"📅 Published: {article['publish_date']}\n")
            f.write(f"✍️ Authors: {', '.join(article['authors']) if article['authors'] else 'Not specified'}\n")
            f.write(f"🔗 URL: {article['url']}\n\n")
            f.write(article['content'] + "\n\n")
            f.write("■"*100 + "\n\n")
    
    print(f"\n✅ Saved {len(articles)} complete articles to '{filename}'")
    print(f"📂 File location: {os.path.abspath(filename)}")

def main():
    print("📡 Fetching news headlines...")
    raw_articles = fetch_news()
    
    if not raw_articles:
        print("\n🔴 No articles found. Possible solutions:")
        print("1. Try a different network/VPN")
        print("2. Generate a new API key at newsapi.org")
        print("3. Use RSS fallback (run the RSS version instead)")
        return
    
    print(f"\n🔍 Extracting full content for {len(raw_articles)} articles...")
    
    complete_articles = []
    for article in raw_articles:
        print(f"\n🔄 Processing: {article['title'][:70]}...")
        full_article = extract_full_article(article['url'])
        
        if full_article:
            full_article['url'] = article['url']
            full_article['source'] = article['source']['name']
            complete_articles.append(full_article)
            print(f"✔ Extracted {len(full_article['content'].split())} words")
        else:
            print("❌ Failed to extract full content")
        
        time.sleep(3)  # Be polite with delays
    
    if complete_articles:
        save_full_articles(complete_articles)
    else:
        print("❌ Couldn't extract any complete articles")

if __name__ == "__main__":
    print("="*60)
    print("🇮🇳 INDIAN NEWS EXTRACTOR - FULL ARTICLE VERSION")
    print("="*60)
    main()