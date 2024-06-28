#!/bin/bash
project="fnic-2024"
region="europe-west1"
comm="lemmydirectory@lemmy.dbzer0.com"
mod_user="fnicmodbot"
mod_pw="fnicmodbot-db0:latest"
gist="94127e24dc129210db8dfb819dd8d6b1"
ghtoken="gh-fnic-bot-gist:latest"

gcloud run jobs deploy bestofbot-fnic --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_fnic_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_fnic_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="💭 ❗Top Imaginary Network posts of the week❗ 💭" --set-secrets="BOTPW=best_of_fnic_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-generalart --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_generalart_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_generalart_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="🎨 ❗Top General Artworks posts of the week❗ 🎨" --set-secrets="BOTPW=best_of_generalart_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-photo --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_photo_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_photography_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="📷❗Top Photography posts of the week❗📷" --set-secrets="BOTPW=best_of_photo_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-themes --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_themes_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_themes_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="🖼️❗Top Themes posts of the week❗🖼️" --set-secrets="BOTPW=best_of_themes_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-comics --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_comics_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_comics_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="❗Top Comics posts of the week❗" --set-secrets="BOTPW=best_of_comics_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-wallpapers --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_wallpapers_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/_wallpaper_comms.json",MODUSER="$mod_user",IMAGES_ONLY=1,NSFW_BEHAVIOUR=2,GIST=$gist,POSTTITLE="❗Top Wallpaper posts of the week❗" --set-secrets="BOTPW=best_of_wallpaper_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken" &
gcloud run jobs deploy bestofbot-anime --project=$project --region=$region --source . --set-env-vars=BOTUSER="moebot",BOTINSTANCE="ani.social",COMMUNITY="$comm",COMMLIST="configs/_anime_comms.json",IMAGES_ONLY=1,NSFW_BEHAVIOUR=1,GIST=$gist,POSTTITLE="💢❗Top Anime Art posts of the week❗💢" --set-secrets="BOTPW=moebot:latest,GHTOKEN=$ghtoken"
wait
