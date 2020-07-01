import json
import discord
import helpers
import markov
import random
import datetime

# boot up activities

h = helpers.Helpers()
h.logger("Starting up.", "Info")
# settings and api keys oh my
conf_file = open("config//config_secret.json", "rt+")
config = json.load(conf_file)
conf_file.close()
# create the markov chainer
m = markov.MarkovChainer(2)
h.markov_startup(m)
# create the bot object
bot = discord.Client()


# Discord Bot Event Handlers
# on_message() = any time a text message shows up in a text channel the bot can access
# msg is the context of the message, and msg.content is the actual text body
@bot.event
async def on_ready():
    print("Vaporwave George Costanza has logged the fuck in.")
    h.logger("Startup: The bot is alive with the sounds of music. Connected to Discord API on "
             + str(datetime.datetime.now()), "Info")


@bot.event
async def on_disconnect():
    h.logger("The bot has disconnected from discord... This could be because the script failed in a fatal way, "
             "or a connection issue", "Warn")


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.content == "george.help":
        await msg.channel.send("HELLO BOBCHANNEL. I'm Vaporwave George Costanza. I'm a discord bot built by Micolithe "
                               "that replicates some of the old IRC bot's functions. For transparency **I am scraping "
                               "all public channels for input** for the markov chainer. I do two main things. Random "
                               "gibberish sentences and replace a random word with butt.")
        return
    h.markov_add(m, msg.content, config["markov_excluded_words"])
    if str(msg.channel) not in config["talk_in"]:
        # print(str(msg.channel) + " not equal to " + str(config["talk_in"]))
        return
    # print(str(msg.author) + " : " + msg.content)  # Just so I can see what's coming in
    rng_calculator = random.randrange(1, 30)
    h.logger("Calculated a random number : " + str(rng_calculator), "Info")
    # print(str(rng_calculator))
    if rng_calculator == 10:
        h.logger("RNG = 10, Butt Replace function activated", "Info")
        # do the butt replace
        butt = h.butt_replace(msg.content)
        print(butt)
        if butt is not None:
            await msg.channel.send(butt)
        return
    elif rng_calculator == 20:
        h.logger("RNG = 20, Markov Gibberish function activated", "Info")
        markov_string = m.generate_sentence()
        await msg.channel.send(markov_string)
        return


if __name__ == "__main__":
    bot.run(config["discord_token"])
