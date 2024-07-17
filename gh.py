#!/usr/bin/python3
from github import Github
from github import Auth
from github import InputFileContent

def gist_update(filename, contents, gist, auth):
  if gist != 0:
    auth = Auth.Token(auth)
    g = Github(auth=auth)
    try:
      gist = g.get_gist(gist)
    except Exception as e:
      print(f'Cannot get gist: {e}')
      return

    try:
      gist.edit(files = {f'{filename}': InputFileContent(content=contents)})
    except Exception as e:
      print(f'Cannot post Gist: {e}')
