#!/usr/bin/python3
from invidious.enums import ContentType
from invidious import *
import urllib.parse as urlparse
from urllib.parse import parse_qs
import shorten
import ssl

def get(url, rapidkey):
  parsed = urlparse.urlparse(url)
  qs = parse_qs(parsed.query)

  if (url[:17] != 'https://youtu.be/') and (url[:20] != 'https://youtube.com/') and (url[:24] != 'https://www.youtube.com/'):
    if 'v' not in qs:
      return None

  try:
    _create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
    pass
  else:
    ssl._create_default_https_context = _create_unverified_https_context

  if 'v' in qs:
    id = qs['v']

  if parsed.netloc == 'youtu.be':
    id = parsed.path[1:]

  try:
    iv = Invidious(mirrors = ['https://invidious.nerdvpn.de'])
  except Exception as e:
    print({e})
    return None

  print(id)

  vid = iv.get_video(video_id = id, region = 'GB')
  print(vid)

  l = iv.search(id)
  print(l)

  #t = ''

  #if yt.thumbnail_url is not None:
  #  t = f'![]({yt.thumbnail_url})\n\n'
  #if yt.title is not None:
  #  t += f'*{yt.title}*\n\n'
  #else:
  #  print('no title')
  #  return None
  #if yt.description is not None:
  #  t += shorten.shorten_text(yt.description, rapidkey)
  #return t

get('https://youtu.be/T_Ig2rqhK28?si=SSY7m5gnEKYPU2Yn', None)

