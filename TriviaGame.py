from Game import Game

class TriviaGame(Game):
    def __init__(self, channel):
        super().__init__(channel)
        self.question = None
        self.answers = []
        self.correct_answer = None

    async def start(self):
        # Set the question and answers
        self.question = "What is the capital of France?"
        self.answers = ["Paris", "London", "Berlin", "Rome"]
        self.correct_answer_index = 0  # Index of the correct answer (Paris)

        # Send the question to the channel
        self.message = await self.channel.send(
            f"Trivia time! Question: {self.question}\n"
            "React with the corresponding emoji:\n"
            "🇦) Paris\n🇧) London\n🇨) Berlin\n🇩) Rome"
        )

        # Add reactions to the message
        reactions = ["🇦", "🇧", "🇨", "🇩"]
        for reaction in reactions:
            await self.message.add_reaction(reaction)

    async def handle_reaction(self, reaction, user):
        if reaction.message.id != self.message.id:
            return

        # Map emoji to answer indices
        emoji_to_index = {"🇦": 0, "🇧": 1, "🇨": 2, "🇩": 3}
        if reaction.emoji not in emoji_to_index:
            return

        selected_index = emoji_to_index[reaction.emoji]
        if selected_index == self.correct_answer_index:
            await self.channel.send(f"{user.display_name} answered correctly!")
        else:
            await self.channel.send(
                f"{user.display_name} answered incorrectly."
            )

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            self.channel.send("Correct!")
        else:
            self.channel.send("Incorrect. The correct answer is Paris.")
