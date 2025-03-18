#!/usr/bin/python3
from pytubefix import YouTube
import urllib.parse as urlparse
from urllib.parse import parse_qs
import shorten

def get(url, rapidkey):
  yt = None

  if (url[:17] != 'https://youtu.be/') and (url[:20] != 'https://youtube.com/') and (url[:24] != 'https://www.youtube.com/'):
    parsed = urlparse.urlparse(url)
    if 'v' not in parse_qs(parsed.query):
      return None

  proxy = {
    "http": "socks5://18.135.211.182:3128",
    "https": "socks5://18.135.211.182:3128"
  }

  try:
    yt = YouTube(url, proxies=proxy)
  except Exception as e:
    print({e})
    return None

  t = ''

  if yt.thumbnail_url is not None:
    t = f'![]({yt.thumbnail_url})\n\n'
  if yt.title is not None:
    t += f'*{yt.title}*\n\n'
  else:
    print('no title')
    return None
  if yt.description is not None:
    t += shorten.shorten_text(yt.description, rapidkey)
  return t
