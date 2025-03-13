import requests
from bs4 import BeautifulSoup
import json

def check_alignment_forum():
    url = "https://www.alignmentforum.org/allPosts?sortedBy=new"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print all div classes to find the correct post container
    print("All div classes found:")
    for div in soup.find_all('div', class_=True):
        print(f"Class: {div['class']}")
        
    # Try to find posts with different potential class names
    potential_classes = ['PostsItem2', 'PostsItem', 'posts-item', 'post-item']
    for class_name in potential_classes:
        posts = soup.find_all('div', class_=class_name)
        print(f"\nFound {len(posts)} posts with class '{class_name}'")
        
        if posts:
            print("\nFirst post structure:")
            print(posts[0].prettify())

if __name__ == "__main__":
    check_alignment_forum() 