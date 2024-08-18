#!/usr/bin/python3

import requests

def extract(apikey, article_url):

  if 'bandcamp.com' in article_url:
    return None

  url = "https://news-article-data-extract-and-summarization1.p.rapidapi.com/extract/"

  payload = { "url": article_url }
  headers = {
	"x-rapidapi-key": apikey,
	"x-rapidapi-host": "news-article-data-extract-and-summarization1.p.rapidapi.com",
	"Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  r = response.json()

  if "summary" in r:
    sum = ''
    if r['summary'] is None:
      return None
    for s in r['summary']:
      sum += f' {s}'
    sum += ' 🖊️'
  elif "description" in r:
    sum = r['description']
  else:
    return None

  pt = '\n'
  if "topImage" in r:
    pt += f'![]({r["topImage"]})\n\n'

  pt += f'*{r["title"]}*\n\n{sum}\n\n'

  return pt


