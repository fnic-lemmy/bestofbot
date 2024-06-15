#!/usr/bin/python3

import json
import sys
import string
import random
import urllib.parse
from pythorhead import Lemmy
from pythorhead.types import SortType

def sortfunc(e):
  return e['score']

def get_commlist(cfg):
  try:
    with open(cfg) as f:
      commlist = json.load(f)
      commlist.sort()
      return commlist

  except Exception as e:
    print("error reading config file: {e}")
    return None

def gen_shield(c):
  cenc = urllib.parse.quote_plus(c)
  return f'![Lemmy](https://img.shields.io/lemmy/{cenc}?style=flat-square&label=Subscribers)'


def run(user, pw, instance, postcomm, cfg, post_title):
  topposts = 0
  toppost = []

  noposts = 0
  nopostsc = []

  lemmy = Lemmy(f'https://{instance}', raise_exceptions=True, request_timeout=30)
  try:
    lemmy.log_in(user, pw)
  except Exception as e:
    print(f'login failed: {e}\n')
    sys.exit(1)

  communities = get_commlist(cfg)
  if communities is None:
    print('no communities')
    sys.exit(1)

  for comm in communities:
    try:
      community_id = lemmy.discover_community(comm)
    except Exception as e:
      print(f'discover {comm} failed: {e}\n')

    if community_id is not None:
      try:
        lemmy.community.follow(community_id) # ensure we get new posts
      except Exception as e:
        print(f'cannot follow {comm}: {e}\n')

      try:
        posts = lemmy.post.list(community_id = community_id, limit = 5, sort = SortType.TopWeek)
      except Exception as e:
        print(f'cannot get posts for {comm}: {e}\n')

      if (len(posts) > 0):
        for p in posts:
          if('url' in p['post']):
            toppost.append(0)
            toppost[topposts] = {}
            toppost[topposts]['post'] = p['post']
            toppost[topposts]['score'] = p['counts']['score']
            toppost[topposts]['community'] = comm
            toppost[topposts]['author'] = p['creator']
            topposts += 1

            break
      else:
        print(f"no posts in {comm} this week")
        nopostsc.append(0)
        nopostsc[noposts] = comm
        noposts += 1
      
    else:
      print(f"cannot find {comm}\n")

  toppost.sort(reverse = True, key = sortfunc)

  found = False
  if (len(nopostsc) > 0):
    comm = random.choice(nopostsc)
    try:
      community_id = lemmy.discover_community(comm)
    except:
      print(f'cannot discover {comm}: {e}\n')
    if community_id is not None:
      for sorttype in [SortType.TopMonth, SortType.TopYear, SortType.TopAll]:
        try:
          posts = lemmy.post.list(community_id = community_id, limit = 5, sort = sorttype)
        except Exception as e:
          print(f'cannot get posts in {comm}: {e}\n')

        if (len(posts) > 0):
          for p in posts:
            if('url' in p['post']):
              toppost.append(0)
              toppost[topposts] = {}
              toppost[topposts]['post'] = p['post']
              toppost[topposts]['score'] = p['counts']['score']
              toppost[topposts]['community'] = comm
              toppost[topposts]['author'] = p['creator']
              topposts += 1

              found = True

              break

        if found is True:
          break

  posttext = ''
  n = 0

  for p in toppost:
    n += 1
    # check if this is a random inactive community
    lemmyverselink = "https://lemmyverse.link/" + p['post']['ap_id'][8:]
    if (n < len(toppost)) or (found is False):
      shield = gen_shield(p['community'])
      posttext = posttext + f"## {n}. [{p['post']['name']}]({lemmyverselink}) ([direct link]({p['post']['ap_id']})) ({p['score']})\n\n!{p['community']} {shield}\n\n" 
    else:
      posttext = posttext + f'\n----\n## Inactive communities 👻\n\nThese communities have had no posts in the last week:\n\n'
      for c in nopostsc:
        shield = gen_shield(c)
        posttext = posttext + f'* !{c} {shield}\n\n'

      posttext = posttext + "\n\nHere is a popular post from one of the inactive communities. 🪦♻️\n\n"
      posttext = posttext + f"[{p['post']['name']}]({lemmyverselink}) ([direct link]({p['post']['ap_id']})), posted in !{p['community']} ({p['score']})\n\n"
      
    posttext = posttext + f"![]({p['post']['url']})\n\n"
    posttext = posttext + f"Posted by [{p['author']['name']}]({p['author']['actor_id']})\n\n"
  
  print(posttext)

  if postcomm is None:
    sys.exit(0)

  try:
    community_id = lemmy.discover_community(postcomm)
  except Exception as e:
    print(f'cannot discover {postcomm}: {e}')
    sys.exit(1)

  if community_id is not None:
    '''post'''
    try:
      post = lemmy.post.create(community_id, post_title, url=toppost[0]['post']['url'], body=posttext)
    except Exception as e:
      print(f'cannot post, exception = {e}\n')
      sys.exit(0) # say we succeeded as it tends to fail (timeout) but post anyway

    try:
      comment = lemmy.comment.create(post["post_view"]["post"]["id"], "Please comment under the original posts.  The main links are using lemmyverse.link which should redirect to the post on your own instance. If you have not used this before, you may need to go direct to https://lemmyverse.link/ and click on 'configure instance'.  Some apps will open posts correctly when using the direct link.\n\nIf you have a comment about the weekly posts please create a [META] post in the community.  Thanks!")
    except Exception as e:
      print(f'cannot post comment, exception = {e}\n')
      # not critical - continue
      
    try:
      lock = lemmy.post.lock(post["post_view"]["post"]["id"], True)
    except Exception as e:
      print(f'cannot lock post, exception = {e}\n')
      # not critical - exit with success code
      sys.exit(0)
