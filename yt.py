#!/usr/bin/python3
from pytubefix import YouTube
import urllib.parse as urlparse
from urllib.parse import parse_qs
import shorten
import ssl

def get(url, rapidkey):
  yt = None

  if (url[:17] != 'https://youtu.be/') and (url[:20] != 'https://youtube.com/') and (url[:24] != 'https://www.youtube.com/'):
    parsed = urlparse.urlparse(url)
    if 'v' not in parse_qs(parsed.query):
      return None

  try:
    _create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
    pass
  else:
    ssl._create_default_https_context = _create_unverified_https_context

  try:
    yt = YouTube(url)
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
