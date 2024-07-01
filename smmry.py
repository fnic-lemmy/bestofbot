#!/usr/bin/python3
from asyncio import run
import smmrpy

def smmry(apikey, url, title):

  try:
    sm = smmrpy.SMMRPY(apikey)
    article = run(sm.get_smmry(url=url, length=1))
  except Exception as e:
    print(f'smmry failed: {e}')

  if article is not None:
    if article.title is not None:
      t = f'*{article.title}*\n\n{article.content}\n\n'
    else:
      t = f'{article.content}\n\n'
  else:
    return None

  return t
