import discord
from discord.ext import commands, tasks
import asyncio
import random
import os

# Function to read token from file
def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Function to read random messages from the text file
def read_quotes_from_file(file_path):
    with open(file_path, 'r') as file:
        quotes = file.readlines()
    return [quote.strip() for quote in quotes]

# Function to read forbidden words from the text file
def read_forbidden_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words]

# This line is how the bot gets the discord token, please put the token in the token file
current_directory = os.path.dirname(os.path.abspath(__file__))
token_file_path = os.path.join(current_directory, "token")
TOKEN = read_token_from_file(token_file_path)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

# Path to the text files containing quotes and forbidden words, please make changes to the files directly
quotes_file_path = os.path.join(current_directory, "Quotes")
bad_words_file_path = os.path.join(current_directory, "BadWords")
random_messages = read_quotes_from_file(quotes_file_path)
forbidden_words = read_forbidden_words_from_file(bad_words_file_path)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    delete_messages.start()
    drink_random_message.start()

@bot.command()
async def deletetrash(ctx):
    await ctx.message.delete()
    await ctx.send('Deleting all messages in this channel...')
    await asyncio.sleep(2)  # Optional delay to let users see the confirmation message
    await ctx.channel.purge()
    await ctx.send("I'm taking out the trash :3")

@tasks.loop(hours=3)
async def delete_messages():
    channel_id = CHANNEL_ID_HERE  # Replace this with the ID of the channel you want to delete messages from
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.purge()
        await channel.send("I'm taking out the trash :3")

@tasks.loop(minutes=30)
async def drink_random_message():
    channel_id = CHANNEL_ID_HERE  # Replace this with the ID of the channel where you want to send the message
    channel = bot.get_channel(channel_id)
    if channel:
        message = random.choice(random_messages)
        await channel.send(message)

@bot.command(name="menu")
async def help_menu(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!deletetrash", value="Deletes all messages in the channel", inline=False)
    embed.add_field(name="!badwords", value="Shows the list of forbidden words", inline=False)
    embed.add_field(name="!shitpost", value="Posts a random shitpost", inline=False)
    embed.add_field(name="!menu", value="Shows this message", inline=False)
    embed.set_footer(text="With love from Swoftii <3")

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def addword(ctx, *, word):
    forbidden_words.append(word.lower())
    await ctx.send(f'Added "{word.lower()}" to the list of forbidden words.')

@addword.error
async def addword_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

@bot.command(name="badwords")
@commands.has_permissions(administrator=True)
async def forbidden_words_command(ctx):
    embed = discord.Embed(
        title="List of Forbidden Words",
        description="\n".join(forbidden_words),
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def shitpost(ctx):
    message = random.choice(random_messages)
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Don't send any message if command is not found
    else:
        await ctx.send("An error occurred while processing the command.")

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Ignore messages sent by the bot itself
        return

    for word in forbidden_words:
        if word in message.content.lower():
            await message.channel.send(f"{message.author.mention} YOU CAN'T SAY THAT WORD >:c")
            break

    await bot.process_commands(message)  # This line ensures that commands still work properly

bot.run(TOKEN)

# Version 1.1 | <3 | Swoftii
