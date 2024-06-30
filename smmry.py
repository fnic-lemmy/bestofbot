#!/usr/bin/python3
from asyncio import run
import smmrpy

def smmry(apikey, url):

  try:
    sm = smmrpy.SMMRPY(apikey)
    article = run(sm.get_smmry(url=url, length=1))
  except Exception as e:
    print(f'smmry failed: {e}')

  t = f'*{article.title}*\n\n{article.content}\n\n'
  return t
