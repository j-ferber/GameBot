from Game import Game
import random
class TriviaGame(Game):
    def __init__(self, channel, gm):
        super().__init__(channel, gm)
        self.question = None
        self.answers = []
        self.correct_answer = None

    async def start(self):
        # List of questions with their possible answers and the index of the correct answer
        trivia_questions = [
            {
                "question": "What is the capital of France?",
                "answers": ["Paris", "London", "Berlin", "Rome"],
                "correct_index": 0
            },
            {
                "question": "What is the largest planet in our solar system?",
                "answers": ["Earth", "Mars", "Jupiter", "Saturn"],
                "correct_index": 2
            },
            {
                "question": "Who wrote 'To Kill a Mockingbird'?",
                "answers": ["Harper Lee", "Mark Twain", "Ernest Hemingway", "F. Scott Fitzgerald"],
                "correct_index": 0
            },
            {
                "question": "What is the chemical symbol for water?",
                "answers": ["H2O", "O2", "CO2", "NaCl"],
                "correct_index": 0
            },
            {
                "question": "Which element has the atomic number 1?",
                "answers": ["Helium", "Oxygen", "Hydrogen", "Carbon"],
                "correct_index": 2
            },
            {
                "question": "What is the tallest mountain in the world?",
                "answers": ["K2", "Kangchenjunga", "Lhotse", "Mount Everest"],
                "correct_index": 3
            }
        ]

        # Randomly select a question
        selected_question = random.choice(trivia_questions)
        self.question = selected_question["question"]
        self.answers = selected_question["answers"]
        self.correct_answer_index = selected_question["correct_index"]

        # Create the message with the question and answers
        answer_emojis = ["🇦", "🇧", "🇨", "🇩"]
        answer_text = "\n".join([f"{emoji}) {answer}" for emoji, answer in zip(answer_emojis, self.answers)])
        self.message = await self.channel.send(
            f"Trivia time! Question: {self.question}\n"
            "React with the corresponding emoji:\n"
            f"{answer_text}"
        )

        # Add reactions for answers
        for emoji in answer_emojis:
            await self.message.add_reaction(emoji)

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
            self.score(user, 5)
        else:
            await self.channel.send(f"{user.display_name} answered incorrectly.")

        self.gm.end_game(self)

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer:
            self.channel.send("Correct!")
        else:
            self.channel.send("Incorrect. The correct answer is Paris.")
        self.gm.end_game(self)
