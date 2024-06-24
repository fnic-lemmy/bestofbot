#!/bin/bash
gcloud run jobs deploy bestofbot-fnic --project=fnic-2024 --region=europe-west1 --source . --set-env-vars=BOTUSER="best_of_fnic_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="lemmydirectory@lemmy.dbzer0.com",COMMLIST="_fnic_comms.json",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,POSTTITLE="💭 ❗Top Imaginary Network posts of the week❗ 💭" --set-secrets="BOTPW=best_of_fnic_bot:latest"
gcloud run jobs deploy bestofbot-anime --project=fnic-2024 --region=europe-west1 --source . --set-env-vars=BOTUSER="moebot",BOTINSTANCE="ani.social",COMMUNITY="lemmydirectory@lemmy.dbzer0.com",COMMLIST="_anime_comms.json",IMAGES_ONLY=1,NSFW_BEHAVIOUR=1,POSTTITLE="❗Top Anime Art posts of the week❗" --set-secrets="BOTPW=moebot:latest"
