import random
import discord
from Game import Game
import asyncio
import os
import json

class DiceGame(Game):
    def __init__(self, channel, gm):
        super().__init__(channel, gm)
        self.roll_result = None
        self.message = None

    async def start(self):
        self.roll_result = random.randint(1, 6)
        print(self.roll_result)

        self.message = await self.channel.send('Guess the roll result! React with 1️⃣, 2️⃣, 3️⃣, 4️⃣, 5️⃣, or 6️⃣.')

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
        for reaction in reactions:
            await self.message.add_reaction(reaction)

    async def handle_reaction(self, reaction, user):
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
        if reaction.message.id != self.message.id:
            return
        if user == self.gm.bot.user:
            return
        if str(reaction.emoji) not in reactions:
            return

        guess = reactions.index(str(reaction.emoji)) + 1
        if guess == self.roll_result:
            await self.channel.send(f'🎉 Correct! The roll was {self.roll_result}.')
            self.score(user, 10)
        else:
            await self.channel.send(f'❌ Incorrect. The roll was {self.roll_result}.')

        # Send the roll result to the channel
        await self.channel.send(f"The dice rolled a {self.roll_result}!")
        self.gm.end_game(self)
