# bestofbot

This bot scans a set of Lemmy communities to find the highest rated post in the last week. 

It posts to `/c/lemmydirectory@lemmy.dbzer0.com` on the schedule in the following calendar:
https://use10.thegood.cloud/apps/calendar/p/dFMpSoX7FPf6EyYX

History is also posted here in case the post to Lemmy fails:
https://gist.github.com/fnic-bot/94127e24dc129210db8dfb819dd8d6b1

---
deploy.sh contains the configuration items as follows:

```
gc_deploy "**category**" "**images_only**" "**title" "**category-subcategory**"
```

The JSON file holds the list of communities to scan.
The Lemmy bot password is a pointer to an entry in Google Secret Manager - it is not the password itself.

NSFW behaviours are; (you need to use the full command to set this currently)
- 0 - mark as nsfw if one post is nsfw
- 1 - always mark as nsfw
- 2 - skip nsfw posts

The bot will deploy on commits to the main branch by automatically running deploy.sh
