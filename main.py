import sys
import os
import bestof
import gh

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)

BOTUSER = os.getenv("BOTUSER",0)
BOTPW = os.getenv("BOTPW", 0)
BOTINSTANCE = os.getenv("BOTINSTANCE", 0)
POSTCOMMUNITY = os.getenv("COMMUNITY", 0)
COMMUNITIES = os.getenv("COMMLIST", 0)
TITLE = os.getenv("POSTTITLE", 0)
IMAGESONLY = os.getenv("IMAGES_ONLY", 0)
NSFW = os.getenv("NSFW_BEHAVIOUR", 0)
MODUSER = os.getenv("MODUSER",0)
MODPW = os.getenv("MODPW", 0)
GIST = os.getenv("GIST", 0)
GHTOKEN = os.getenv("GHTOKEN", 0)
TLDRTHIS_APIKEY = os.getenv("TLDRTHIS_API", 0)
SMMRY_APIKEY = os.getenv("SMMRY_API", 0)

def main(user, pw, inst, comm, cfg, title, imgs, nsfw, moduser, modpw, gist, ghtoken, tldr_api, smmry_api):

    io = False

    if imgs == 1:
      io = True

    try:
      contents = bestof.run(user, pw, inst, comm, cfg, title, io, nsfw, moduser, modpw, tldr_api, smmry_api)
    except Exception as e:
      print(f'err: {e}')

    if contents is not None:
      fn = cfg.split('/')[1].split('.')[0]
      gh.gist_update(f'{fn}.md', contents, gist, ghtoken)

    return "bestofbot"

# Start script
if __name__ == "__main__":
    try:
        main(BOTUSER, BOTPW, BOTINSTANCE, POSTCOMMUNITY, COMMUNITIES, TITLE,
             int(IMAGESONLY), int(NSFW), MODUSER, MODPW, GIST, GHTOKEN, TLDRTHIS_APIKEY, SMMRY_APIKEY)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(message)
        sys.exit(1)  # Retry Job Task by exiting the process

