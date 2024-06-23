# bestofbot

This bot scans a set of Lemmy communities to find the highest rated post in the last week. 

deploy.sh contains the configuration items as follows:

```
gcloud run jobs deploy **bot-name**
--project=fnic-2024 --region=europe-west1 --source .
--set-env-vars=BOTUSER="**lemmy-user**",
BOTINSTANCE="**lemmy-instance**",
COMMUNITY="**community-to-post-in**",
COMMLIST="**json-file-listing-communities**",
IMAGES_ONLY=1,
NSFW_BEHAVIOUR=0,
POSTTITLE="**post-title**"
--set-secrets="BOTPW=**lemmy-password**:latest"
```

The JSON file holds the list of communities to scan.
The Lemmy bot password is a pointer to an entry in Google Secret Manager - it is not the password itself. 
NSFW behaviours are;
0 - mark as nsfw if one post is nsfw
1 - always mark as nsfw

The bot will deploy on commits to the main branch by automatically running deploy.sh

