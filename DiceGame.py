import random
from Game import Game

class DiceGame(Game):
    def __init__(self, channel, gm):
        super().__init__(channel, gm)
        self.roll_result = None

    async def start(self):
        # Simulate rolling a 6-sided dice
        self.roll_result = random.randint(1, 6)
        
        # Send the roll result to the channel
        await self.channel.send(f"The dice rolled a {self.roll_result}!")
        self.gm.end_game(self)
