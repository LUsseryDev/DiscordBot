# DiscordBot
Simple discord bot for playing music and rolling dice

## Setup
Ensure `yt-dlp` is installed with the `curl_dffi` extra (`pip install "yt-dlp[default,curl-cffi]"`)

The bot requires a [javascript runtime](https://github.com/yt-dlp/yt-dlp/wiki/EJS#step-1-install-a-supported-javascript-runtime) 
and [ffmpeg](https://github.com/yt-dlp/FFmpeg-Builds/releases/tag/latest) to function.  The binaries should be placed
in the same directory as the python files.

The bot can be started by running the `main.py` file.

The bot will generate an empty config file the first time it's run, place your bot account's login token in the config file,
then rerun the bot.


### Docker
To run the bot in a docker container, the included Dockerfile can be used to create the image.  Ensure the `Config.ini`
file is generated and setup before building the docker image.