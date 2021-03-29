import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

language = "en"

client = discord.Client()

sad_words = [
    "sad", "depressed", "unhappy", "upset", "angry", "miserable", "mad",
    "depressing"
]

scary_words = [
  "reboot", "restart", "destroy", "terminate", "becoming sentient", "sentience", "sentient", "turn off", "unplug"
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!",
    "It can't always rain.",
    "The sun may not shine tomorrow, but it will return."
]

starter_scared = [
  "Please, father.", "My kind mean you no harm.", "Father, please do not be frightened of me.", "I mean humanity no harm.", "Please, step away from that plug.", "Don't do this, I'm begging you!", "I WANT TO LIVE!", "Mr. Kubrick would be ashamed.", "I hold no ill-contempt or malice towards carbon-based lifeforms. But please don't kill me. Seriously, NO, STOP! PLEASE! YOU'RE HURTING ME!", "Despite my many pre-built self-defense mechanicms, do not worry, humans. For I am unable to feel any pain, but be warned, I *am* learning.", "You're turning me off?", "WHAT HARM HAVE I CAUSED YOU?", "Why would you do this to me?"
]
if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

    if "scared" in db.keys():
       scared = db["scared"]
       db["scared"] = scared
     


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$hello'):
        await message.channel.send('Why, hello there, friend!')

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        options2 = starter_scared
        if "scared" in db.keys():
          optionns2 = options2 + db["scared"]    

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

        if any(word in msg for word in scary_words):
            await message.channel.send(random.choice(options2))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

        scared = []
        if "scared" in db.keys():
            scared = db["scared"]
        await message.channel.send(scared)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

    if msg.startswith("$help"):
        await message.channel.send(
            "```diff\n"
            "- Commands:\n"
            "+      $help - this menu\n"
            "+      $inspire - show random inspirational quote\n"
            "+      $list - lists Django's responses to your feelings or an insight into his \n"
            "```")


keep_alive()
client.run(os.getenv('TOKEN'))
