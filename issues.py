#!/usr/bin/python3
from github import Github
from github import Auth
from github import Repository

def raise_issue(ghtoken, ghrepo, title, desc):

  auth = Auth.Token(ghtoken)
  g = Github(auth=auth)
  repo = g.get_repo(ghrepo)
  my_issues = repo.get_issues(state = "open", creator = "fnic-bot")
  for issue in my_issues:
    print(issue)
    if issue.title == title:
      print('already raised')
      issue.create_comment(f'This has failed again.\n\n{desc}')
      return

  i = repo.create_issue(title = title, body = desc, labels = [repo.get_label(name = "community")])
