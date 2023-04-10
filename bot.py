import os
from asyncio import sleep
import requests

import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import c_dict
import json
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='#', intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot online as username {bot.user}')

@bot.command(name='help')
async def help(ctx):
    em = discord.Embed(title="A list of commands",
                       color=discord.Color.purple())
    em.add_field(name='#countries', value='List all the countries we have in our database.', inline=False)
    em.add_field(name='#c_destinations [country name]', value='List the tourist destinations of a specific country.', inline=False)
    em.add_field(name='#weather [city]', value='Show the weather of a city using both Celsius and Fahrenheit.', inline=False)
    em.add_field(name='#randomc', value='Pick a random country for you!', inline=False)
    em.add_field(name='#quote', value='Generate a random motivational quote!', inline=False)
    em.add_field(name='#trips', value='See the current trips you have planned.', inline=False)
    em.add_field(name='#addtrip [name (no spaces)] [location] [start date] [end date]', value='Add a new trip to your plan.', inline=False)
    em.add_field(name='#removetrip [name]', value='Remove the trip from your list', inline=False)
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)

@bot.command(name='countries')
async def countries(ctx):
    em = discord.Embed(title="A list of countries!",
                       color=discord.Color.purple())
    for key in c_dict.countries_dict:
        em.add_field(name=key, value=c_dict.countries_dict[key]["description"], inline=False)
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)

@bot.command(name='c_destinations')
async def countries_destinations(ctx, country):
    if country not in c_dict.countries_dict:
        await ctx.send("Not a country in our database! (Remember to capitalize every word in the country's name, and use underscore for spaces!)")
        return
    em = discord.Embed(title="Tourist destinations of " + country,
                       color=discord.Color.purple())
    em.add_field(name="Tourist destinations: ", value=c_dict.countries_dict[country]["tourist destinations"], inline=False)
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    em.set_thumbnail(url=c_dict.countries_dict[country]["image"])
    await ctx.send(embed=em)

@bot.command(name='weather')
async def weather(ctx, city):
    city_name = city
    complete_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + os.getenv('API_KEY') + "&q=" + city_name
    response = requests.get(complete_url)
    if response.json()["cod"] != "404":
        y = response.json()["main"]
        ct = y["temp"]
        ctc = str(round(ct - 273.15))
        ctf = str()
        cp = y["pressure"]
        ch = y["humidity"]
        z = response.json()["weather"]
        w_desc = z[0]["description"]
        em = discord.Embed(title=f"Weather in {city_name}",
                              color=discord.Color.purple())
        em.add_field(name="Description", value=f"**{w_desc}**", inline=False)
        em.add_field(name="Temperature",value=f"**{ctc}°C**", inline=False)
        em.add_field(name="Humidity(%)", value=f"**{ch}%**", inline=False)
        em.add_field(name="Atmospheric Pressure(hPa)", value=f"**{cp}hPa**", inline=False)
        em.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        em.set_footer(text=f"Information requested by {ctx.author.name}!")
        await ctx.send(embed=em)
    else:
        await ctx.send("City not found.")

@bot.command(name='randomc')
async def randomc(ctx):
    em = discord.Embed(title="Your Random Country",
                       color=discord.Color.purple())
    country = random.choice(list(c_dict.countries_dict.keys()))
    em.add_field(name=f"{country}", value=f"Description: {c_dict.countries_dict[country]['description']}")
    em.set_thumbnail(url=c_dict.countries_dict[country]["image"])
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)

@bot.command(name='quote')
async def get_quote(ctx):
  with open("quotes.txt") as f:
    numlines = sum(1 for _ in f)
  target_line = random.choice(range(0, numlines-1, 2))
  with open("quotes.txt") as f:
      for _ in range(target_line):
          next(f)
      topic = next(f)
  em = discord.Embed(title="A Random Quote:",
                     color=discord.Color.purple())
  em.add_field(name="Quote: ", value=f"{topic}")
  em.set_footer(text=f"Information requested by {ctx.author.name}!")
  await ctx.send(embed=em)

@bot.command(name='trips')
async def trips(ctx):
    user = ctx.author
    await open_account(user)
    users = await get_data()
    em = discord.Embed(title="Current trips",
                       color=discord.Color.purple())

    for key in users[str(user.id)]:
        em.add_field(name=key, value=f"Location:{str(users[str(user.id)]['Location'])}\nStart date: {str(users[str(user.id)][key]['start'])}\nEnd date:{str(users[str(user.id)][key]['end'])}")
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)
    return True

@bot.command(name="addtrip")
async def addtrip(ctx, name, location, start, end):
    user = ctx.author
    await open_account(user)
    users = await get_data()

    users[str(user.id)][name] = {
        "Location": location,
        "start": start,
        "end": end
    }
    print(users[str(user.id)][name])
    em = discord.Embed(title="Add a trip!",
                       color=discord.Color.purple())
    em.add_field(name="Trip added successfully!", value=f"Location:{users[str(user.id)][name]['Location']}\nStart date: {users[str(user.id)][name]['start']}\nEnd date:{users[str(user.id)][name]['end']}")
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)
    with open("tripcentral.json", "w") as f:
        json.dump(users, f)
    return True

@bot.command(name="removetrip")
async def removetrip(ctx, name):
    user = ctx.author
    await open_account(user)
    users = await get_data()
    del users[str(user.id)][name]
    em = discord.Embed(title="Delete a trip!",
                       color=discord.Color.purple())
    em.add_field(name="Trip added successfully!",
                 value=f"Deleted on {datetime.date}.")
    em.set_footer(text=f"Information requested by {ctx.author.name}!")
    await ctx.send(embed=em)
    with open("tripcentral.json", "w") as f:
        json.dump(users, f)
    return True



async def open_account(user):
    users = await get_data()
    users = await get_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}

    with open("tripcentral.json", 'w') as f:
        json.dump(users, f)
    return True
async def get_data():
    with open("tripcentral.json", 'r') as f:
        users = json.load(f)
    return users

bot.run(TOKEN)