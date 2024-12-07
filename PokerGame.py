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
        msg = f"Your Poker Hand:\n{str(self.hand)}\n\nWhat cards would you like to redraw?"
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
            #await self.channel.send(f"{user.display_name} has confirmed their selection.")
            await self.redraw(user, self.selected_indices)  # Return the list of selected indices
            return

        # Add the selected index if it's not already in the list
        if selected_index not in self.selected_indices:
            self.selected_indices.append(selected_index)
            #await self.channel.send(f"{user.display_name} selected card index {selected_index + 1}.")

    async def redraw(self, user, selected_indices):
        self.selection = selected_indices
        self.selection.sort(reverse=True)
        numCardsRemoved = len(self.selection)
        for i in self.selection:
            self.hand.pop(i)
            #instead of popping, just set equal to new card.
        self.hand = self.pickCards(self.hand, self.deck, numCardsRemoved)
        msg = f"Your New Poker Hand:\n{str(self.hand)}\n"
        await self.channel.send(msg)
        await self.checkHand(user)

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
    
    async def checkHand(self, user):
        msg = "\n"
        values = [card[0] for card in self.hand]
        suits = [card[1] for card in self.hand]
        value_counts = {value: values.count(value) for value in set(values)}

        if len(set(suits)) == 1:
            msg += "You have a Flush! Score increased by 5!"
            self.score(user, 5)
        elif 4 in value_counts.values():
            msg += "You have Four of a Kind! Score increased by 10!"
            self.score(user, 10)
        elif 3 in value_counts.values() and 2 in value_counts.values():
            msg += "You have a Full House! Score increased by 7!"
            self.score(user, 7)
        elif 3 in value_counts.values():
            msg += "You have Three of a Kind! Score increased by 3!"
            self.score(user, 3)
        elif list(value_counts.values()).count(2) == 2:
            msg += "You have Two Pairs! Score increased by 2!"
            self.score(user, 2)
        elif 2 in value_counts.values():
            msg += "You have One Pair! Score increased by 1!"
            self.score(user, 1)
        else:
            msg += "You have Junk."

        await self.channel.send(msg)

