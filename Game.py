from abc import ABC, abstractmethod
import asyncio
import os
import json

class Game(ABC):
    def __init__(self, channel, gm):
        """
        Initializes the Game with a channel where it will be played.
        """
        self.channel = channel
        self.active = True
        self.gm = gm

    @abstractmethod
    async def start(self):
        """
        This method will be overridden by subclasses to start the specific game.
        It must be implemented in any subclass of Game.
        """
        pass

    def end(self):
        """
        End the game and mark it as no longer active.
        """
        self.active = False
        asyncio.create_task(self.channel.send("The game has ended!"))

    def is_active(self):
        """
        Returns whether the game is still active.
        """
        return self.active  

    def score(self, user):
        """
        Updates the score of the user in the game.
        """
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []
        else:
            scores = []

        username = str(user)
        user_found = False
        for entry in scores:
            if entry['username'] == username:
                entry['score'] += 1
                user_found = True
                break

        if not user_found:
            scores.append({'username': username, 'score': 1})

        with open('data.json', 'w') as f:
            json.dump(scores, f, indent=4)