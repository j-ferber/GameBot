from TriviaGame import TriviaGame
from DiceGame import DiceGame
from PokerGame import PokerGame

class GameManager:
    def __init__(self, bot):
        self.bot = bot
        self.games = []

    async def start_game(self, channel, game_type):
        if game_type == 'trivia':
            game = TriviaGame(channel, self)
        elif game_type == 'dice':
            game = DiceGame(channel, self)
        elif game_type == 'poker':
            game = PokerGame(channel, self)
        
        self.games.append(game) 
        await game.start()

    def get_active_games(self):
        return [game for game in self.games if game.is_active()]
    
    def end_game(self, game):
        self.games.remove(game)
        game.end()