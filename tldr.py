#!/usr/bin/python3

import requests

def tldrthis(apikey, article_url):

  url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-url/"

  payload = {
	  "url": article_url,
	  "min_length": 100,
	  "max_length": 300,
	  "is_detailed": False
  }
  headers = {
  	"x-rapidapi-key": apikey,
  	"x-rapidapi-host": "tldrthis.p.rapidapi.com",
	  "Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  r = response.json()

  if "summary" in r:
    #print(f'{r["article_title"]}\n\n{r["summary"][0]} {r["article_image"]}')

    pt = "\n"
    if "article_image" in r:
      pt += f'![]({r["article_image"]})\n\n'

    pt += f'*{r["article_title"]}*\n\n{r["summary"][0]} 🖋️\n\n'

    return pt
  return None

