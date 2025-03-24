import discord
import json
import random
import asyncio
import aiofiles
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

url = "https://raw.githubusercontent.com/owenwillette/trivia/refs/heads/main/triviaquestions.json"
response = requests.get(url)
trivia_questions = response.json()

for q in trivia_questions:
    print(q["question"])
    for i, option in enumerate(q["options"], start=1):
        print(f"{i}. {option}")
# Load scores from a JSON file
async def load_scores():
    try:
        async with aiofiles.open("scores.json", mode="r") as file:
            return json.loads(await file.read())
    except FileNotFoundError:
        return {}

# Save scores to a JSON file
async def save_scores(scores):
    async with aiofiles.open("scores.json", mode="w") as file:
        await file.write(json.dumps(scores, indent=4))

questions = []
scores = {}
current_question = None
current_answer = None
@bot.command()
async def leaderboard(ctx):
    scores = await load_scores()
    
    if not scores:
        await ctx.send("Answer some trivia to get on the leaderboard.")
        return

    leaderboard_text = "**Leaderboard**\n"
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for i, (user, score) in enumerate(sorted_scores, start=1):
        leaderboard_text += f"{i}. {user} - {score} points\n"

    await ctx.send(leaderboard_text)

@bot.command()
async def hint(ctx):
    if current_question:
        hint_letter = current_question["options"][current_answer][0]  # First letter of the correct answer
        await ctx.send(f"Hint: The correct answer starts with **{hint_letter}**")
    else:
        await ctx.send("No active question right now!")

async def post_trivia_question():
    await bot.wait_until_ready()
    channel = bot.get_channel(https://discord.com/channels/1330021981487108219/1341066942907158569)
    while not bot.is_closed():
        global current_question, current_answer
        current_question = random.choice(trivia_questions)
        current_answer = current_question["answer"]
        await channel.send(f"Trivia Question: {current_question['question']}")
        await asyncio.sleep(3600)  # Post every hour

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!answer'):
        answer = message.content.split(' ', 1)[1]
        if answer.lower() == current_question["options"][current_answer].lower():
            await message.channel.send("Correct!")
            scores[message.author.name] = scores.get(message.author.name, 0) + 1
            await save_scores(scores)
        else:
            await message.channel.send("Incorrect. Try again!")

    await bot.process_commands(message)
    
bot.loop.create_task(post_trivia_question())
