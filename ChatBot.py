# import required packages
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
import yaml

# create ChatBot
chatBot = ChatBot('ChatBot')

# Use the Closest Match Adapter logic adapter to match the best result at 90% accuracy.
chatBot.logic_adapters = [
    {
        'import_path': 'chatterbot.logic.ClosestMatchAdapter',
        'default_response': 'I am sorry, but I do not understand.',
        'maximum_similarity_threshold': 0.90  # Threshold to match
    }
]

# create ChatBot trainer
trainer = ChatterBotCorpusTrainer(chatBot)

# Train ChatBot with English language corpus
# you can train with different language
# or with your custom .yam file
trainer.train("C:\\Unit4\\testbot\\weatherBotdata.yml")

# Greeting from chat bot
print("Hi, I am ChatBot")

# keep communicating with ChatBot
while True:
    # take user input/query
    query = input(">>>")

    # response from ChatBot
    response = (chatBot.get_response(Statement(text=query, search_text=query)))

