import discord
import json
import random
import asyncio
import aiofiles
from discord.ext import commands
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
        await ctx.send(f"🧐 Hint: The correct answer starts with **{hint_letter}**")
    else:
        await ctx.send("No active question right now!")
