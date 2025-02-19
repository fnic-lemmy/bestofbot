#!/bin/bash
project="fnic-2024"
region="europe-west1"
comm="lemmydirectory@lemmy.dbzer0.com"
mod_user="fnicmodbot"
mod_pw="fnicmodbot-dbzer0:latest"
ghrepo="fnic-lemmy/lemmy-directory"
ghtoken="fnic-bot-issues:latest"
nsfw="2"

gc_deploy() {
  gcloud run jobs deploy bestofbot-$4 --project=$project --region=$region --source . --set-env-vars=BOTUSER="best_of_$1_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="$comm",COMMLIST="configs/$4.json",MODUSER="$mod_user",IMAGES_ONLY=$2,NSFW_BEHAVIOUR=$5,GHREPO="$ghrepo",POSTTITLE="$3" --set-secrets="BOTPW=best_of_$1_bot:latest,MODPW=$mod_pw,GHTOKEN=$ghtoken,TLDRTHIS_API=rapidapi:latest" &
}

gc_deploy_quick() {
  if [ -z "$3" ]; then
    title="❗Top $1 posts of the month❗"
  else
    title="$3"
  fi

  gc_deploy "$1" "$2" "$title" "$1" "$nsfw"
}

gc_deploy_quick "fnic" "1" "💭 ❗Top Imaginary Network posts of the month❗ 💭"
gc_deploy_quick "generalart" "1" "🎨 ❗Top General Artworks posts of the month❗ 🎨"
gc_deploy_quick "photo" "1" "📷❗Top Photography posts of the month❗📷"
gc_deploy_quick "themes" "0" "🖼️❗Top Themes posts of the month❗🖼️"
gc_deploy_quick "comics" "1"
gc_deploy_quick "wallpapers" "1"
gc_deploy "ai" "0" "❗Top AI Art posts of the month❗" "ai" "1"
gc_deploy_quick "animals" "0"
gc_deploy_quick "music" "0" "🎵❗Top Music (General discussion) posts of the month❗🎵"
gc_deploy "music" "0" "🎵❗Top Music (Genres) posts of the month❗🎵" "music-genres" "$nsfw"
gc_deploy "gaming" "0" "❗Top Gaming (Platforms) posts of the month❗" "gaming-platforms" "$nsfw"
gc_deploy "gaming" "0" "❗Top Gaming (Genres) posts of the month❗" "gaming-genres" "$nsfw"
gc_deploy "gaming" "0" "❗Top Gaming (General) posts of the month❗" "gaming-general" "$nsfw"
gc_deploy "memes" "1" "❗Top Memes (General) posts of the month❗" "memes-general" "$nsfw"
gc_deploy "memes" "0" "❗Top Memes (News) posts of the month❗" "memes-news" "$nsfw"
gc_deploy "memes" "1" "❗Top Memes (Shows) posts of the month❗" "memes-shows" "$nsfw"
gc_deploy "memes" "1" "❗Top Memes (Games) posts of the month❗" "memes-games" "$nsfw"
gc_deploy "memes" "1" "❗Top Memes (Social Media) posts of the month❗" "memes-social" "$nsfw"

gcloud run jobs deploy bestofbot-anime --project=$project --region=$region --source . --set-env-vars=BOTUSER="moebot",BOTINSTANCE="ani.social",COMMUNITY="$comm",COMMLIST="configs/anime.json",IMAGES_ONLY=1,NSFW_BEHAVIOUR=1,GHREPO="$ghrepo",POSTTITLE="💢❗Top Anime Art posts of the month❗💢" --set-secrets="BOTPW=moebot:latest,GHTOKEN=$ghtoken" &
wait
