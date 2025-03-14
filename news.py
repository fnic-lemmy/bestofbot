#!/usr/bin/python3
from newspaper import Article
from newspaper import Config
import shorten
import nltk

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


def article(url, rapidkey):
  config = Config()
  config.browser_user_agent = "Mozilla/5.0"

  art = Article(url)
  try:
    art.download()
  except Exception as e:
    print(f'unable to download article, {e}')
    return None
  art.parse()
  nltk.download('punkt')
  nltk.download('punkt_tab')
  art.nlp()
  t = ''
  if art.top_image is not None:
    t = f'![]({art.top_image})\n\n'
  if art.title is not None:
    t += f'*{art.title}*\n\n'
  if (art.summary is not None) and (len(art.summary) > 0):
    t += f'{art.summary} 🖊️️🤖\n\n'
  elif art.text is not None:
    t += shorten.shorten_text(art.text, rapidkey)
  if len(t) > 0:
    return t
    
  return None
