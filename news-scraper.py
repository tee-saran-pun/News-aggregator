import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Request the URL
url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSFFpZ0FQAQ/sections/..."
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Step 2: Extract Titles, Links, and Author
titles = []
links = []
authors = []

# Find all articles
articles = soup.find_all('article')

# Extract the title, link, and author from each article
for article in articles:
    # Find the <a> tag containing the title and link
    title_tag = article.find('a', class_='JtKRv')
    
    if title_tag:
        # Extract the title text
        title = title_tag.text.strip()
        titles.append(title)
        
        # Extract the link (relative URL)
        link = "https://news.google.com" + title_tag['href'][1:]
        links.append(link)
    
    # Find the author inside the <span> tag (if available)
    author_tag = article.find('span')
    if author_tag:
        author = author_tag.text.strip()
        authors.append(author)
    else:
        authors.append('No author available')

# Step 4: Save the data to a CSV file
news_df = pd.DataFrame({
    'Title': titles,
    'Link': links,
    'Author': authors
})

# Try saving the CSV file
try:
    news_df.to_csv('google_news_articles.csv', index=False)
    print("File saved successfully.")
except Exception as e:
    print(f"Error saving file: {e}")
