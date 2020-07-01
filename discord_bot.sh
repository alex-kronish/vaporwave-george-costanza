#!/bin/bash
#change the cd command to wherever the code for the bot is
#then add this shell script to your crontab file
#you cant use dot slash in crontab so just do /bin/sh /path/to/discord_bot.sh instead
cd /home/media/bots/discord/
PROCESSIDCHECK=$(ps ax | grep -v grep | grep discord_bot.py)
if [ -z "$PROCESSIDCHECK" ]
then
  echo "Can't find Georgie. Starting the bot..."
  eval "python3 ./discord_bot.py"
else
  echo "Bot still running. We're ok!"
fi