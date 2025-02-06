#!/usr/bin/python3

import requests

def shorten(text, key, max_len):
  url = "https://deepseek-v3.p.rapidapi.com/chat"

  payload = { "messages": [
		{
			"role": "user",
			"content": f"Please shorten the following text to less than {max_len} characters, only returning the shortened text:\n{text}"
		}
	] }
  headers = {
	"x-rapidapi-key": key,
	"x-rapidapi-host": "deepseek-v3.p.rapidapi.com",
	"Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  r = response.json()
  print(r)
  return r['content']
