import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.utils import get
from discord.ext import commands
from requests import get

from bs4 import BeautifulSoup
import re

token = os.environ['token']

client = commands.Bot(command_prefix = "$") 

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "bad", "blue", "brokenhearted", "cast down", "crestfallen", "dejected", "depressed", "despondent", "disconsolate", "doleful", "down", "downcast", "downhearted", "down in the mouth", "droopy", "forlorn", "gloomy", "glum", "hangdog", "heartbroken", "heartsick", "heartsore", "heavyhearted", "inconsolable", "joyless", "low", "low-spirited", "melancholic", "melancholy", "miserable", "mournful", "saddened", "sorrowful", "sorry", "unhappy", "woebegone", "woeful", "wretched"]

starter_encouragements = ["Try, try, try and try again. Feed your mind ideas of success, not failure", "Remember, the only way you can fail is if you give up. Every time you fail, you come one step closer to success", "You are not scared; you are courageous. You are not weak; you are powerful. You are not ordinary; you are remarkable", "Do not back down, do not give up", "When you look back on your life, don't have regrets. Believe in yourself, belief in your future, you will find your way", "A fire burning inside you is mighty; it is waiting to burn bright. You are meant to do great things", "Following your dreams can be both terrifying and exciting", "Courage is facing fear. Fear of failure holds most people back. You are not most people", "Persist and persuade others about your plans, as they are real. Nobody can do this but you. Nobody will get in the way of our dreams", "Go for your dreams; it is your turn"]

if "responding" not in db.keys():
  db["responding"] = True

#function that gets random zen quotes
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    if quote.startswith("Too many requests"):
      quote = random.choice(starter_encouragements)
    return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) < index:
    del encouragements[index]
    db["encouragements"] = encouragements

#prints out in the log whenever bot successfully logs in
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#reads in messages from the channel that is not from the bot
@client.event
async def on_message(message):
  if message.author==client:
    return
  msg = message.content
  # athr = message.author
  hmuchannel = client.get_channel(921954463982440469)

  if msg.startswith('$help'):
    await hmuchannel.send('Commands: \n $meme, $abml, $bbb, $inspire, $new, $del, $list, $responding')
    
  if msg.startswith('$bbb'):
    await hmuchannel.send('Bing Bong!!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
      
  gamingwords = "Val val valorant Valorant league League LoL"
  if msg in gamingwords:
    await message.channel.send("there is no passion, there is no vision, there is no aggression, there is no fking mindset in this discord, what the hell is there in the discord")

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("responding ", 1) [1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("BBB is on! ;)")
    else:
      db["responding"] = False
      await message.channel.send("BBB is off! :C")

  if msg.startswith("$meme"):
    print("posting meme")
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await message.channel.send(embed=meme)

  if msg.startswith("$abml"):
    print("calling abml method")
    url = 'https://www.google.com/finance/quote/ABML:OTCMKTS?sa=X&ved=2ahUKEwjc3KPNvJP1AhUqnuAKHc3gD0cQ3ecFegQIJxAc'
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'lxml')
    regex = re.compile('.*YMlKec fxKbKc.*') #what html component to find
    current_price = soup.find('div', {'class': regex}).text
    current_price = re.sub(r'.', '', current_price, count = 1)
    if (float(current_price) < 1.10):
      await message.channel.send("dont look unless you want to cry: " + current_price)
    elif (float(current_price) > 1.20):
      print(current_price + ' THATS WHAT I LIKE TO SEE, LFG!!: '+current_price)
    else:
      print(current_price + ' not too shabby')

keep_alive()
client.run(token)
