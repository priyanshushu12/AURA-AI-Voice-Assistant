import requests
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
import key

# Function to fetch news from Currents API
def fetch_current_news_currents(api_key, query="latest news", language="en", page_size=5, country=None):
    url = 'https://api.currentsapi.services/v1/latest-news'

    params = {
        'apiKey': api_key,
        'language': language,
        'page_size': page_size,
        'query': query
    }

    if country:
        params['country'] = country

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()

        if news_data.get("status") == "ok":
            return news_data.get("news", [])
        else:
            print("Failed to fetch news from Currents API.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from Currents API: {e}")
        return []

# Function to fetch news from NewsAPI
def fetch_recent_news_newsapi(api_key, query="latest news", days=5):
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"from={from_date}&"
        f"to={to_date}&"
        f"sortBy=publishedAt&"
        f"apiKey={api_key}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

        if news_data.get("status") == "ok":
            return news_data.get("articles", [])
        else:
            print("Failed to fetch news from NewsAPI.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from NewsAPI: {e}")
        return []

# Function to filter news based on topic
def filter_news_by_topic(articles, topic):
    topic_keywords = {
        'technology': ['technology', 'tech', 'AI', 'gadgets', 'software', 'IT'],
        'sports': ['sports', 'football', 'cricket', 'basketball', 'tennis'],
        'politics': ['politics', 'government', 'election', 'policy'],
        'health': ['health', 'medicine', 'wellness', 'disease'],
        'economy': ['economy', 'finance', 'stock market', 'GDP'],
        'entertainment': ['entertainment', 'movies', 'music', 'celebrities'],
        'science': ['science', 'research', 'discovery'],
        'environment': ['environment', 'climate', 'pollution', 'sustainability']
    }

    keywords = topic_keywords.get(topic.lower(), [])
    if not keywords:
        print(f"No keywords found for the topic '{topic}'.")
        return []

    filtered_articles = [
        article for article in articles
        if any(keyword in (article.get('title', '') + article.get('description', '')).lower() for keyword in keywords)
    ]

    return filtered_articles

# Function to merge and display the best news
def merge_and_display_best_news(currents_articles, newsapi_articles, topic, page_size=5):
    combined_articles = currents_articles + newsapi_articles

    seen_articles = set()
    unique_articles = []

    for article in combined_articles:
        unique_identifier = (
            article.get('title', '').lower(),
            article.get('url', '').lower()
        )
        if unique_identifier not in seen_articles:
            unique_articles.append(article)
            seen_articles.add(unique_identifier)

    sorted_articles = sorted(
        unique_articles, key=lambda x: x.get('published', ''), reverse=True
    )

    if sorted_articles:
        print(f"\nTop {page_size} news articles on '{topic}':\n")
        for i, article in enumerate(sorted_articles[:page_size], start=1):
            title = article.get('title', 'No Title')
            if article.get('language') != 'en':
                title = GoogleTranslator(source='auto', target='en').translate(title)

            source = article.get('source', {}).get('name', 'Unknown Source')
            published_at = article.get('published', 'No Date')
            url = article.get('url', '#')

            print(f"{i}. {title}")
            print(f"   Source: {source}")
            print(f"   Published At: {published_at}")
            print(f"   URL: {url}\n")
    else:
        print(f"No articles found for the topic '{topic}'.")

# Main function
def main():
    CURRENTS_API_KEY =key.CURRENTS_API_KEY
    NEWS_API_KEY = key.NEWS_API_KEY

    print("Welcome to the News Aggregator!")
    topic = input("Enter a topic (e.g., technology, sports, politics, etc.): ").strip().lower()

    valid_topics = ['technology', 'sports', 'politics', 'health', 'economy', 'entertainment', 'science', 'environment']
    if topic not in valid_topics:
        print(f"Invalid topic. Please choose from: {', '.join(valid_topics)}.")
        return

    try:
        page_size = int(input("How many articles do you want to see? ").strip())
        if page_size <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    country_code = input("Enter a country code (e.g., 'us' for USA, 'in' for India) or leave blank: ").strip().lower()

    currents_articles = fetch_current_news_currents(
        CURRENTS_API_KEY, query=topic, language="en", page_size=page_size, country=country_code
    )
    newsapi_articles = fetch_recent_news_newsapi(NEWS_API_KEY, query=topic, days=5)

    currents_articles = filter_news_by_topic(currents_articles, topic)
    newsapi_articles = filter_news_by_topic(newsapi_articles, topic)

    merge_and_display_best_news(currents_articles, newsapi_articles, topic, page_size)


