#!/usr/bin/python3

import requests

def shorten(text, key, max_len):
  url = "https://deepseek-v31.p.rapidapi.com/"

  payload = {
        "model": "deepseek-v3",
        "messages": [
		{
			"role": "user",
			"content": f"Shorten the following text to {max_len} characters. Return only the shortened text without adding, interpreting, or modifying the meaning. Do not include explanations or notes. Text:\n{text}"
		}
	] }
  headers = {
	"x-rapidapi-key": key,
	"x-rapidapi-host": "deepseek-v31.p.rapidapi.com",
	"Content-Type": "application/json"
  }

  response = requests.post(url, json=payload, headers=headers)

  r = response.json()
  print(r)
  return r['content']
