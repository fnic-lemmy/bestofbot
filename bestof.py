#!/usr/bin/python3

import json
import sys
import string
import random
import tldr
import smmry
import yt
import urllib.parse
from urllib.parse import urlparse
from pythorhead import Lemmy
from pythorhead.types import SortType

def sortfunc(e):
  return e['score']

def get_commlist(cfg):
  try:
    with open(cfg) as f:
      commlist = json.load(f)
      #commlist.sort()
      return commlist

  except Exception as e:
    print("error reading config file: {e}")
    return None

def get_comminfo(lemmy, c):
  try:
    id = lemmy.discover_community(c)
  except Exception as e:
    print(f'cannot discover {c}: {e}')
    return None

  return lemmy.community.get(id)["community_view"]["community"]

def extract_desc(ci):
  if "description" in ci:
    desc = ci["description"]
    d = desc.splitlines()
    for l in d:
      if (len(l) > 0):
        if (l[:1] != '#') and (l[:1] != '-') and (l[:1] != '*'):
          return l

  return "No description"

def gen_shield(c):
  mbin = [ 'fedia.io',
           'kbin.social'
         ]

  dom = c.split('@')[1]
  if dom in mbin:
    serv = "mbin"
  else:
    serv = "lemmy"

  cenc = urllib.parse.quote_plus(c)
  return f'![{serv}](https://img.shields.io/{serv}/{cenc}?style=flat&label=Subs&color=pink)'


def run(user, pw, instance, postcomm, cfg, post_title, images_only, nsfw_b, moduser, modpw, tldrkey, smmrykey):
  topposts = 0
  toppost = []

  noposts = 0
  nopostsc = []

  nsfw = False

  if nsfw_b == 1:
    # force nsfw
    nsfw = True

  skip_urls = ["rabbitea.rs", "file.coffee"]

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

      found = False

      if (len(posts) > 0):
        for p in posts:
          if p['post']['nsfw'] is True:
            if nsfw_b == 2:
              continue

          if('url' in p['post']):
            if images_only is True:
              if 'url_content_type' in p['post']:
                # if there's no url_content_type we accept it regardless
                mime = p['post']['url_content_type']
                if(mime[:5] != "image") and (mime[:11] != "application"):
                  continue
              else:
                print(f'no mime type for {p["post"]["id"]}')

            found = True
            break

          else:
            if images_only is True:
              continue
            else:
              found = True
              break

      if found is True:
        if p['post']['nsfw'] is True:
          nsfw = True
        toppost.append(0)
        toppost[topposts] = {}
        toppost[topposts]['post'] = p['post']
        toppost[topposts]['score'] = p['counts']['score']
        toppost[topposts]['community'] = comm
        toppost[topposts]['comminfo'] = p['community']
        toppost[topposts]['author'] = p['creator']
        topposts += 1

      if found is not True:
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
            if p['post']['nsfw'] is True:
              if nsfw_b == 2:
                continue

            if('url' in p['post']):
              host = urlparse(p['post']['url'])
              if(host.netloc in skip_urls):
                print(f'skipping {host.netloc}\n')
                break
              if images_only is True:
                if 'url_content_type' in p['post']:
                  mime = p['post']['url_content_type']
                  if(mime[:5] != "image") and (mime[:11] != "application"):
                    continue

              found = True
              break

            else:
              if images_only is True:
                continue
              else:
                found = True
                break

          if found is True:
            if p['post']['nsfw'] is True:
              nsfw = True
            toppost.append(0)
            toppost[topposts] = {}
            toppost[topposts]['post'] = p['post']
            toppost[topposts]['score'] = p['counts']['score']
            toppost[topposts]['community'] = comm
            toppost[topposts]['comminfo'] = p['community']
            toppost[topposts]['author'] = p['creator']
            topposts += 1
            break

  posttext = ''
  n = 0

  for p in toppost:
    n += 1
    # set nsfw tag
    if p['post']['nsfw'] is True:
      nsfw_txt = "[**NSFW**]"
    else:
      nsfw_txt = ""
    # check if this is a random inactive community
    lemmyverselink = "https://lemmyverse.link/" + p['post']['ap_id'][8:]
    if (n < len(toppost)) or (found is False):
      shield = gen_shield(p['community'])
      title = p['comminfo']['title'].strip()
      posttext = posttext + f"### {n}. [{p['post']['name']}]({lemmyverselink}) {nsfw_txt} ([direct link]({p['post']['ap_id']})) ({p['score']})\n\nfrom **{title}** (!{p['community']}) {shield}\n\n"
    else:
      posttext = posttext + f'\n----\n# Inactive communities 👻\n\nThese communities have had no posts in the last week:\n\n'
      for c in nopostsc:
        shield = gen_shield(c)
        comminfo = get_comminfo(lemmy, c)
        posttext = posttext + f'- [{comminfo["title"]}](/c/{c}) {shield}\n'
        commdesc = extract_desc(comminfo)
        if commdesc is not None:
          posttext += f'   - {commdesc}\n'

      posttext = posttext + "\n\n### Here is a popular post from one of the inactive communities. 🪦♻️\n\n"
      posttext = posttext + f"[{p['post']['name']}]({lemmyverselink}) {nsfw_txt} ([direct link]({p['post']['ap_id']})), posted in [{p['comminfo']['title']}](/c/{p['community']}) ({p['score']})\n\n"
    
    #if 'url_content_type' in p['post']:
    #  print(f'{p["post"]["name"]} - {p["post"]["url_content_type"]}')

    if(images_only is True) or ("url_content_type" not in p['post']) or (("url_content_type" in p['post']) and (p['post']['url_content_type'][:5] == "image")):
      posttext = posttext + f"![]({p['post']['url']})\n\n"
    elif "url" in p['post']:
      if "url_content_type" in p['post']:
        if p['post']['url_content_type'][:9] == 'text/html':
          # try youtibe
          t = yt.get(p['post']['url'])
          if t is not None:
            posttext += t
          else:
            # run through tldr
            t = tldr.tldrthis(tldrkey, p['post']['url'])
            if t is not None:
              posttext += t
            else:
              # use smmry
              t = smmry.smmry(smmrykey, p['post']['url'], True)
              if t is not None:
                posttext += t
      else:
        '''no content type'''
    else:
      '''not url'''
      t = smmry.smmry(smmrykey, p['post']['ap_id'], False)
      if t is not None:
        posttext += t

    posttext = posttext + f"Posted by [{p['author']['name']}]({p['author']['actor_id']})\n\n"
  
  posttext += "\n\n----\n\nThe main links are using lemmyverse.link which should redirect to the post on your own instance. If you have not used this before, you may need to go direct to https://lemmyverse.link/ and click on 'configure instance'.  Some apps will open posts correctly when using the direct link."
  print(posttext)

  if nsfw is True:
    print("** nsfw posts detected **")

  if postcomm is None:
    return posttext

  try:
    community_id = lemmy.discover_community(postcomm)
  except Exception as e:
    print(f'cannot discover {postcomm}: {e}')
    sys.exit(1)

  if community_id is not None:
    '''post'''
    try:
      post = lemmy.post.create(community_id, post_title, url=toppost[0]['post']['url'], body=posttext, nsfw=nsfw)
    except Exception as e:
      print(f'cannot post, exception = {e}\n')
      return posttext

    try:
      comment = lemmy.comment.create(post["post_view"]["post"]["id"], "Please comment under the original posts.  \n\nThe descriptions of the inactive communities are auto-generated, it will pick up the first non-header line from the sidebar.\n\nIf you have a comment about the weekly posts please create a [META] post in the community.  Thanks!")
    except Exception as e:
      print(f'cannot post comment, exception = {e}\n')
      # not critical - continue
    
    if moduser != 0:
      # log in as our mod user
      try:
        lemmy.log_in(moduser, modpw)
      except Exception as e:
        print(f'login failed: {e}\n')
        # non-fatal, we'll try with the regular user
    
    try:
      lock = lemmy.post.lock(post["post_view"]["post"]["id"], True)
    except Exception as e:
      print(f'cannot lock post, exception = {e}\n')
      # not critical - exit with success code
      return posttext

  return posttext
  
