#!/bin/bash
gcloud config set project fnic-2024
gcloud run jobs deploy bestofbot-fnic --source . --set-env-vars=BOTUSER="best_of_fnic_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="bot_playground_2@lemmings.world",COMMLIST="_fnic_comms.json" --set-secrets="BOTPW=best_of_fnic_bot:latest"
