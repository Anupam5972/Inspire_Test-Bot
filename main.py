import discord
from discord.ext import tasks
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from random import choice

client = discord.Client()

status = [
    'Jamming out to music!', 'Haaalooo', 'Eating!', 'love', 'Sleeping!',
    'With my Life', '✨✨✨', 'happy', 'Inspire Yourself'
]

sad_words = [
    "sad", "depressed", "horny", "unhappy", "angry", "miserable", "depressing",
    "Happy", "happy"
]

responses = [
    '***grumble*** Why did you wake me up?', 'Top of the morning to you lad!',
    'Hello, how are you?', 'Hi', '**Wasssuup!**'
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$hello"):
        await message.channel.send('Hello There!')

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options += db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

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

    if msg.startswith("$help"):
        await message.channel.send(
            "***`$hello - Encouragement Bot greets you`*** \n ***`$new - Add a new Encouragement Quote`*** \n***`$inspire - Gives out an inspiration Quote to make your day`***\n ***`$list - Shows Encouragements Quotes`*** \n ***`$del {index} - deletes the Encouragements Quotes on the index choosen`*** \n ***`$responding false - Bot will stop responding to the messages`*** \n ***`$responding true - Bot will start responding to the messages`***"
        )

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


keep_alive()
client.run(os.getenv('TOKEN'))
