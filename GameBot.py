# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import json
from GameManager import GameManager

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

gm = GameManager(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name="start_trivia")
async def start_trivia(ctx):
    await ctx.send("Trivia game started! Answer the questions!")
    await gm.start_game(ctx.channel, "trivia")

@bot.command(name="start_dice")
async def start_trivia(ctx):
    await ctx.send("Dice game started!")
    await gm.start_game(ctx.channel, "dice")

@bot.command(name="start_poker")
async def start_poker(ctx):
    await ctx.send("Poker game started!")
    await gm.start_game(ctx.channel, "poker")

@bot.command(name="leaderboard")
async def leaderboard(ctx):
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            try:
                scores = json.load(f)
            except json.JSONDecodeError:
                scores = []
    else:
        scores = []

    top_scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]

    leaderboard_message = "🏆 **Leaderboard** 🏆\n"
    for i, entry in enumerate(top_scores, start=1):
        leaderboard_message += f"{i}. {entry['username']} - {entry['score']} points\n"

    await ctx.send(leaderboard_message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return  
    
    for game in gm.get_active_games():
        if game.channel == reaction.message.channel:
            await game.handle_reaction(reaction, user)


bot.run(os.getenv("token"))