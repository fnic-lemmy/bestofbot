#!/usr/bin/python3

import requests

def shorten(text, key, max_len):
  url = "https://openrouter.ai/api/v1/chat/completions"

  payload = {
        "model": "@preset/bestofbot",
        "messages": [
		{
			"role": "user",
			"content": f"Shorten the following text to {max_len} characters. Text:\n{text}"
		}
	] }
  headers = {
	"Authorization": f"Bearer {key}",
	"Content-Type": "application/json",
	"HTTP-Referer": "https://github.com/fnic-lemmy/bestofbot",
	"X-Title": "BestOfBot - Lemmy Bot",
	"Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  r = response.json()
  print(r)
  return r['choices'][0]['message']['content']


