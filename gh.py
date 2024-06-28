#!/usr/bin/python3
from github import Github
from github import Auth
from github import InputFileContent

def gist_update(filename, contents, gist, auth):
  if gist != 0:

    auth = Auth.Token(auth)
    g = Github(auth=auth)
    gist = g.get_gist(gist)

    gist.edit(files = {filename: InputFileContent(contents)})
