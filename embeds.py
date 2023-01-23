import random
import discord
from discord.ext import commands as disect
import asyncio

print('Embeds Imported')
Prefix = "-"
bot = disect.Bot(command_prefix=Prefix, intents=discord.Intents.all(), case_insensitive=True, self_bot=False)

@bot.command()
async def displaylooping(ctx):
    looping = discord.Embed(
        title='Looping now',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=looping)

@bot.command()
async def displayloopoff(ctx):
    loopoff = discord.Embed(
        title='Disabled Loop',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=loopoff)

@bot.command()
async def displayadded(ctx):
    added = discord.Embed(
        title='Added',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=added)

@bot.command()
async def displayskip(ctx):
    skipped = discord.Embed(
        title='Skipped Song',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=skipped)

@bot.command()
async def displaypause(ctx):
    paused = discord.Embed(
        title='Paused Song',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=paused)

@bot.command()
async def displayresume(ctx):
    resumed = discord.Embed(
        title='Resuming Song',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=resumed)

@bot.command()
async def displaydisconnected(ctx):
    disconnected = discord.Embed(
        title='Disconnected',
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=disconnected)

@bot.command()
async def displaycoinflip(ctx):
    coin = ['Heads','Tails']
    flipcoin = discord.Embed(
        title=random.choice(coin),
        colour=discord.Colour.dark_gold()
    )

    await ctx.send(embed=flipcoin)

