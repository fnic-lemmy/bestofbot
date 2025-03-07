#!/usr/bin/python3
import deepseek

def shorten_text(text, deepseek_key):
  max_len = 300
  if len(text) > max_len:
    print('shorten...')
    try:
      t = deepseek.shorten(text, deepseek_key, max_len)
      t = f'{t} 🖍🤖\n\n'
      return t
    except Exception as e:
      print(f'deepseek raised exception: {e}')
    return f'{text[:297]}...\n\n' # NB: three less than max_len
  else:
    return f'{text}\n\n'
