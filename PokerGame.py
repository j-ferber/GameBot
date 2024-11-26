import random
from Game import Game

class PokerGame(Game):
    def __init__(self, channel, gm):
        super().__init__(channel, gm)
        self.deck = None
        self.hand = None
        self.selection = None

    # async def start(self):
    #     self.round()

    async def start(self):
        self.deck = self.newDeck()
        random.shuffle(self.deck)
        self.hand = self.pickCards(list(), self.deck, 5) # Place 5 cards in hand from deck
        msg = f"Your Poker Hand:\n{str(self.hand)}\n\nWhat cards would you like to keep?"
        self.message = await self.channel.send(msg)
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "✅"]
        for reaction in reactions:
            await self.message.add_reaction(reaction)

    async def handle_reaction(self, reaction, user):
        if reaction.message.id != self.message.id:
            return

        emoji_to_index = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3, "5️⃣": 4, "✅": 5}
        if reaction.emoji not in emoji_to_index:
            return
        
        # Initialize the selected indices list if it doesn't exist
        if not hasattr(self, "selected_indices"):
            self.selected_indices = []

        # Get the index for the emoji
        selected_index = emoji_to_index[reaction.emoji]
        
        # Check if the checkmark is chosen
        if selected_index == 5:  # Checkmark emoji
            await self.channel.send(f"{user.display_name} has confirmed their selection.")
            self.selection = self.selected_indices  # Return the list of selected indices
            return

        # Add the selected index if it's not already in the list
        if selected_index not in self.selected_indices:
            self.selected_indices.append(selected_index)
            await self.channel.send(
                f"{user.display_name} selected card index {selected_index + 1}."
            )

    def newDeck(self):
        deck = []
        for i in range(12):
            for j in range(3):
                card = []
                if i==1:
                    card.append('A')
                elif i==11:
                    card.append('J')
                elif i==12:
                    card.append('Q')
                elif i==0:
                    card.append('K')
                else:
                    card.append(str(i))
                if j==1:
                    card.append('♠')
                elif j==2:
                    card.append('♣')
                elif j==0:
                    card.append('♥')
                else:
                    card.append('♦')
                deck.append(card)
        return deck
    
    def pickCards(self, hand, deck, numCards):
        cardsPicked = random.sample(deck, numCards)
        for card in cardsPicked:
            deck.remove(card)
            hand.append(card)
        return hand

