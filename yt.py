#!/usr/bin/python3
from pytube import YouTube

def get(url):
  yt = None

  if (url[:17] != 'https://youtu.be/') and (url[:20] != 'https://youtube.com/') and (url[:24] != 'https://www.youtube.com/'):
    return None

  try:
    yt = YouTube(url)
  except Exception as e:
    print({e})
    return None

  t = f'![]({yt.thumbnail_url})\n'
  try:
    t += f'*{yt.title}*\n\n'
  except:
    ''' nothing to do '''

  return t
