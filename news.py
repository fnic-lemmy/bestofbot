#!/usr/bin/python3
from newspaper import Article
from newspaper import Config

def article_image(url):
  config = Config()
  config.browser_user_agent = "Mozilla/5.0"

  article = Article(url)
  try:
    article.download()
  except Exception as e:
    print(f'unable to download article, {e}')
    return None
  article.parse()
  if article.top_image is not None:
    return f'![]({article.top_image})\n\n'
  #print(article.summary)
  #print(article.title)
  #print(article.text)

  return None
