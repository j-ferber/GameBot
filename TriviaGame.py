from Game import Game

class TriviaGame(Game):
    def __init__(self, channel, gm):
        super().__init__(channel, gm)
        self.question = None
        self.answers = []
        self.correct_answer = None

    async def start(self):
        self.question = "What is the capital of France?"
        self.answers = ["Paris", "London", "Berlin", "Rome"]
        self.correct_answer_index = 0  # Index of the correct answer (Paris)

        self.message = await self.channel.send(
            f"Trivia time! Question: {self.question}\n"
            "React with the corresponding emoji:\n"
            "🇦) Paris\n🇧) London\n🇨) Berlin\n🇩) Rome"
        )

        reactions = ["🇦", "🇧", "🇨", "🇩"]
        for reaction in reactions:
            await self.message.add_reaction(reaction)

    async def handle_reaction(self, reaction, user):
        emoji_to_index = {"🇦": 0, "🇧": 1, "🇨": 2, "🇩": 3}
        if reaction.message.id != self.message.id:
            return
        if user == self.gm.bot.user:
            return
        if str(reaction.emoji) not in emoji_to_index:
            return

        selected_index = emoji_to_index[str(reaction.emoji)]
        if selected_index == self.correct_answer_index:
            await self.channel.send(f"{user.display_name} answered correctly!")
            self.score(user)
        else:
            await self.channel.send(f"{user.display_name} answered incorrectly.")

        self.gm.end_game(self)

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            self.channel.send("Correct!")
        else:
            self.channel.send("Incorrect. The correct answer is Paris.")
        self.gm.end_game(self)
