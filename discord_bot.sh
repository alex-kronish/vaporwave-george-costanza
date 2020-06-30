#!/bin/bash
PROCESSIDCHECK=$(ps ax | grep -v grep | grep discord_bot.py)
if [ -z "$PROCESSIDCHECK" ]
then
  echo "Can't find Georgie. Starting the bot..."
  eval "python3 ./discord_bot.py"
else
  echo "Bot still running. We're ok!"
fi