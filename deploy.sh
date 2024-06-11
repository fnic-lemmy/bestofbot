#!/bin/bash
gcloud run jobs deploy bestofbot-fnic --project=fnic-2024 --region=europe-west1 --source . --set-env-vars=BOTUSER="best_of_fnic_bot",BOTINSTANCE="lemmy.dbzer0.com",COMMUNITY="bot_playground_2@lemmings.world",COMMLIST="_fnic_comms.json",POSTTITLE="Top Imaginary Network posts last week" --set-secrets="BOTPW=best_of_fnic_bot:latest"
