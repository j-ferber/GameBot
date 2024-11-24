from abc import ABC, abstractmethod
import asyncio

class Game(ABC):
    def __init__(self, channel):
        """
        Initializes the Game with a channel where it will be played.
        """
        self.channel = channel
        self.active = True  

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
