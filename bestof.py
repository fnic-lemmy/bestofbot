#!/usr/bin/python3

import json
import sys
import string
import random
import mimetypes
import tldr
import pipfeed
import yt
import news
import requests
import urllib.parse
import datetime
from urllib.parse import urlparse
from pythorhead import Lemmy
from pythorhead.types import SortType

def sortfunc(e):
  return e['score']['score']

def get_contenttype(url):
  try:
    r = requests.head(url, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
    ct = r.headers['Content-Type']
    print(f'content-type retrieved from URL: {ct}')
    return ct
  except Exception as e:
    print(f'err getting remote content-type: {e}')

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

def shorten_text(text):
  if len(text) > 200:
    return f'{text[:200]}...\n\n'
  else:
    return text

def add_embed(p):
  if "embed_title" in p:
    t = f'*{p["embed_title"]}*\n\n'
  else:
    t = ""
    
  if "embed_description" in p:
    t += f'{p["embed_description"]}\n\n'
  return t
                
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


def run(user, pw, instance, postcomm, cfg, post_title, images_only, nsfw_b, moduser, modpw, rapidkey):
  topposts = 0
  toppost = []

  noposts = 0
  nopostsc = []

  nsfw = False

  if nsfw_b == 1:
    # force nsfw
    nsfw = True

  # add date to post title
  today = datetime.date.today()
  today_text = today.strftime("%d %b %Y")
  post_title += f' ({today_text})'
  print(post_title)

  skip_urls = ["rabbitea.rs", "file.coffee", "sffa.community"]

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
      sys.exit(1) # bomb out so the bot retries

    if community_id is not None:
      try:
        lemmy.community.follow(community_id) # ensure we get new posts
      except Exception as e:
        print(f'cannot follow {comm}: {e}\n')

      try:
        posts = lemmy.post.list(community_id = community_id, limit = 5, sort = SortType.TopMonth)
      except Exception as e:
        print(f'cannot get posts for {comm}: {e}\n')

      found = False

      if (len(posts) > 0):
        for p in posts:
          if ('nsfw' in p['post']) and (p['post']['nsfw']) is True:
            if nsfw_b == 2:
              continue
              
          if p['counts']['score'] < 0:
            break

          if('url' in p['post']):
            if images_only is True:
              if 'url_content_type' in p['post']:
                # if there's no url_content_type we accept it regardless
                mime = p['post']['url_content_type']
              else:
                mime = get_contenttype(p['post']['url'])
                if mime is None:
                  mime, encoding = mimetypes.guess_type(p['post']['url'])
                  print(f'guessed {mime} for {p["post"]["id"]}')
                  if mime is None:
                    found = True
                    break
              # we accept application/octet-stream as cara seems to return it lots, and text/html
              # as Lemmy seems to get a bit confused and use this sometimes.
              if(mime[:5] != "image") and (mime[:11] != "application"):
                continue
              if (mime[:9] == "text/html"):
                # 2nd opinion
                contenttype = get_contenttype(p['post']['url'])
                if contenttype is None:
                  contenttype, encoding = mimetypes.guess_type(p['post']['url'])
                if (contenttype is not None) and contenttype[:5] != "image":
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
        toppost[topposts]['score'] = p['counts']
        toppost[topposts]['community'] = comm
        toppost[topposts]['comminfo'] = p['community']
        toppost[topposts]['author'] = p['creator']
        topposts += 1

      if found is not True:
        print(f"no posts in {comm} this month")
        nopostsc.append(0)
        nopostsc[noposts] = comm
        noposts += 1

    else:
      print(f"cannot find {comm}\n")

  if len(toppost) == 0:
    print('no active communities!')
    try:
      user = lemmy.user.get(username=f'{mod_user}@{instance}')
    except Exception as e:
      print(f'err looking up user {mod_user}@{instance}: {e}')

    if user is not None: 
      try:
        lemmy.private_message.create(content = f'{post_title} was not posted due to no active communities.', recipient_id=user["person_view"]["person"]["id"])
      except Exception as e:
        print(f'err sending PM to {mod_user}@{instance}: {e}')
    sys.exit(0)

  print('sorting...')
  toppost.sort(reverse = True, key = sortfunc)

  found = False
  if (len(nopostsc) > 0):
    comm = random.choice(nopostsc)
    try:
      community_id = lemmy.discover_community(comm)
    except:
      print(f'cannot discover {comm}: {e}\n')
    if community_id is not None:
      for sorttype in [SortType.TopYear, SortType.TopAll]:
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
            toppost[topposts]['score'] = p['counts']
            toppost[topposts]['community'] = comm
            toppost[topposts]['comminfo'] = p['community']
            toppost[topposts]['author'] = p['creator']
            topposts += 1
            break

  posttext = ''
  n = 0

  for p in toppost:
    #print(p['post'])
    n += 1
    
    if "url" in p['post']:
      if "url_content_type" in p['post']:
        if (p['post']['url_content_type'][:5] == "image") or (images_only is True):
          emoji = '🖼️'
        elif (p['post']['url_content_type'][:5] == "video") or ("embed_video_url" in p['post']):
          emoji = '🎦'
        else:
          emoji = '📰'
      elif ("video_embed_url" in p['post']) or (p['post']['url'].endswith(('.avi', '.mp4', '.mpg'))):
        emoji = '🎦'
      elif (p['post']['url'].endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))) or (images_only is True):
        emoji = '🖼️'
      else:
        emoji = '📰'
    else:
      emoji = '💬'

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
      if n > 1:
        posttext += '\n----\n'
      posttext = posttext + f"### {n}. {emoji} [{p['post']['name']}]({lemmyverselink}) {nsfw_txt} ([direct link]({p['post']['ap_id']})) (👍{p['score']['upvotes']}  👎{p['score']['downvotes']})\n\nfrom **{title}** (!{p['community']}) {shield}\n\n"
    else:
      posttext = posttext + f'\n----\n# Inactive communities 👻\n\nThese communities have had no posts in the last month:\n\n'
      for c in nopostsc:
        shield = gen_shield(c)
        comminfo = get_comminfo(lemmy, c)
        posttext = posttext + f'- [{comminfo["title"]}](/c/{c}) {shield}\n'
        commdesc = extract_desc(comminfo)
        if commdesc is not None:
          posttext += f'   - {commdesc}\n'

      posttext = posttext + "\n\n### Here is a popular post from one of the inactive communities. 🪦♻️\n\n"
      posttext = posttext + f"{emoji} [{p['post']['name']}]({lemmyverselink}) {nsfw_txt} ([direct link]({p['post']['ap_id']})), posted in [{p['comminfo']['title']}](/c/{p['community']}) (👍{p['score']['upvotes']}  👎{p['score']['downvotes']})\n\n"
    
    #if 'url_content_type' in p['post']:
    #  print(f'{p["post"]["name"]} - {p["post"]["url_content_type"]}')

    if(images_only is True) or ("url" in p['post'] and (("url_content_type" not in p['post']) or (("url_content_type" in p['post']) and (p['post']['url_content_type'][:5] == "image")))):
      posttext = posttext + f"![]({p['post']['url']})\n\n"
    elif "url" in p['post']:
      print(f"* {p['post']['name']} - {p['post']['url']}")
      if "url_content_type" in p['post']:
        if p['post']['url_content_type'][:9] == 'text/html':
          # try youtube
          print('youtube...')
          t = yt.get(p['post']['url'])
          if t is not None:
            posttext += t
          else:
            # run through tldr
            print('tldr...')
            t = tldr.tldrthis(rapidkey, p['post']['url'])
            if t is not None:
              posttext += t
            else:
              print('pipfeed...')
              t = pipfeed.extract(rapidkey, p['post']['url'])
              if t is not None:
                posttext += t
              else:
                # use news3k to get an article image
                print('news...')
                try:
                  t = news.article_image(p['post']['url'])
                except Exception as e:
                  print(f'failed to use news3k to get article: {e}')
                  t = None
                if t is not None:
                  posttext += t
                # add title/desc from lemmy api
                print('lemmy fallback 1...')
                t = add_embed(p['post'])
                if t is not None:
                  posttext += t
                else:
                  print('lemmy fallback 2...')
                  if 'body' in p['post']:
                    posttext += shorten_text(p['post']['body'])
      else:
        '''no content type'''
        t = add_embed(p['post'])
        if t is not None:
          posttext += t
        else:
          # use news3k to get an article image
          t = news.article_image(p['post']['url'])
          if t is not None:
            posttext += t
          if 'body' in p['post']:
            posttext += shorten_text(p['post']['body'])
    else:
      '''not url'''
      if 'body' in p['post']:
        posttext += shorten_text(p['post']['body'])

    posttext = posttext + f"Posted by [{p['author']['name']}]({p['author']['actor_id']})\n\n"
  
  posttext += "\n\n----\n\nThe main links are using lemmyverse.link which should redirect to the post on your own instance. If you have not used this before, you may need to go direct to https://lemmyverse.link/ and click on 'configure instance'.  Some apps will open posts correctly when using the direct link."

  if images_only is not True:
    posttext += "\n\n️🤖 indicates a summary generated using AI - 🖋️ TLDR This, 🖊️ Pipfeed"

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
      comment = lemmy.comment.create(post["post_view"]["post"]["id"], "Please comment under the original posts.  \n\nThe descriptions of the inactive communities are auto-generated, it will pick up the first non-header line from the sidebar.\n\nIf you have a comment about the monthly posts please create a [META] post in the community.  Thanks!")
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
  
