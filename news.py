#!/usr/bin/python3
from newspaper import Article

def article_image(url):
  article = Article(url)
  try:
    article.download()
  except Exception as e:
    return None
  article.parse()
  if article.top_image is not None:
    return f'![]({article.top_image})\n\n'
  #print(article.summary)
  #print(article.title)

  return None
