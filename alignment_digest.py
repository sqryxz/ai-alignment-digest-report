import os
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# Initialize OpenAI client with DeepSeek base URL
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# Constants
LESSWRONG_RSS = "https://www.lesswrong.com/feed.xml?view=community-rss&karmaThreshold=30"
ALIGNMENT_FORUM_API = "https://www.alignmentforum.org/graphql"
POSTS_PER_SOURCE = 5

def fetch_lesswrong_posts():
    """Fetch latest posts from LessWrong RSS feed"""
    feed = feedparser.parse(LESSWRONG_RSS)
    posts = []
    
    for entry in feed.entries[:POSTS_PER_SOURCE]:
        posts.append({
            'title': entry.title,
            'link': entry.link,
            'content': entry.summary,
            'date': entry.published,
            'source': 'LessWrong'
        })
    
    return posts

def fetch_alignment_forum_posts():
    """Fetch latest posts from AI Alignment Forum using GraphQL API"""
    query = """
    {
      posts(input: {
        terms: {
          view: "new",
          limit: 5
        }
      }) {
        results {
          title
          _id
          contents {
            html
          }
          postedAt
          pageUrl
        }
      }
    }
    """
    
    try:
        response = requests.post(ALIGNMENT_FORUM_API, json={'query': query})
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data.get('data', {}).get('posts', {}).get('results', []):
            # Remove any leading slash from pageUrl
            page_url = post['pageUrl'].lstrip('/') if post['pageUrl'] else ''
            
            posts.append({
                'title': post['title'],
                'link': f"https://www.alignmentforum.org/{page_url}",
                'content': BeautifulSoup(post['contents']['html'], 'html.parser').get_text() if post['contents'] else "",
                'date': datetime.fromisoformat(post['postedAt'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                'source': 'AI Alignment Forum'
            })
        
        return posts
    except Exception as e:
        print(f"Error fetching AI Alignment Forum posts: {e}")
        return []

def summarize_post(post):
    """Summarize a post using DeepSeek"""
    prompt = f"""Please provide a concise summary (2-3 sentences) of the following AI alignment-related post. 
    Focus on the key ideas and implications for AI alignment:
    
    Title: {post['title']}
    Content: {post['content'][:2000]}  # Limit content length for API
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",  # Using DeepSeek-V3 model
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in AI alignment research."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_key_themes_summary(posts):
    """Generate a summary of key themes from all posts"""
    print("Generating key themes summary...")
    
    # Create a combined text of all titles and summaries
    combined_text = "\n\n".join([
        f"Title: {post['title']}\nSummary: {summarize_post(post)}"
        for post in posts
    ])
    
    prompt = f"""Based on these AI alignment posts, identify and summarize the 3-4 main themes or key developments discussed across them. 
    Focus on connections between posts and broader implications for AI alignment research and development.
    Format your response in markdown bullet points.

    Posts:
    {combined_text}
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in AI alignment research."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_digest():
    """Generate daily digest of AI alignment posts"""
    print("Generating daily digest...")
    
    # Create digests directory if it doesn't exist
    os.makedirs('digests', exist_ok=True)
    
    # Fetch posts
    lesswrong_posts = fetch_lesswrong_posts()
    print(f"Fetched {len(lesswrong_posts)} posts from LessWrong")
    
    alignment_forum_posts = fetch_alignment_forum_posts()
    print(f"Fetched {len(alignment_forum_posts)} posts from AI Alignment Forum")
    
    all_posts = lesswrong_posts + alignment_forum_posts
    
    # Sort posts by date
    all_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate digest content
    digest_date = datetime.now().strftime('%Y-%m-%d')
    digest_content = f"# AI Alignment Daily Digest - {digest_date}\n\n"
    
    # Add key themes summary
    print("Generating key themes summary...")
    themes_summary = generate_key_themes_summary(all_posts)
    digest_content += "## Key Themes and Developments\n\n"
    digest_content += f"{themes_summary}\n\n---\n\n"
    digest_content += "## Individual Post Summaries\n\n"
    
    # Add individual post summaries
    for post in all_posts:
        print(f"Summarizing: {post['title']}")
        summary = summarize_post(post)
        digest_content += f"### {post['title']}\n"
        digest_content += f"Source: {post['source']}\n"
        digest_content += f"Link: {post['link']}\n\n"
        digest_content += f"Summary: {summary}\n\n"
        digest_content += "---\n\n"
    
    # Save digest
    filename = f"digests/digest_{digest_date}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(digest_content)
    
    print(f"Digest saved to {filename}")

def main():
    """Main function to run the digest generator"""
    # Generate digest immediately on startup
    generate_digest()
    
    # Schedule daily digest generation
    schedule.every().day.at("00:00").do(generate_digest)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 