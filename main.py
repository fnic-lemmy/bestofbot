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

def main(user, pw, inst, comm, cfg, title, imgs, nsfw, moduser, modpw, gist, ghtoken):

    io = False

    if imgs == 1:
      io = True

    contents = bestof.run(user, pw, inst, comm, cfg, title, io, nsfw, moduser, modpw)
    if contents is not None:
      gh.gist_update(f'{cfg}.md', contents, gist, ghtoken)
      
    return "bestofbot"

# Start script
if __name__ == "__main__":
    try:
        main(BOTUSER, BOTPW, BOTINSTANCE, POSTCOMMUNITY, COMMUNITIES, TITLE, int(IMAGESONLY), int(NSFW), MODUSER, MODPW, GIST, GHTOKEN)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(message)
        sys.exit(1)  # Retry Job Task by exiting the process

