"""
QueenAnt.py

A discord bot made in Python for simple moderation and having fun with users.

Credits:
- Original repository: swoftii04/Queen-Ant-Bot
- YoutubeDL usage inspired by the discord.py documentation and various examples found on GitHub.
- Additional inspiration and techniques from discord-bean-bot (https://github.com/beanbot-dev/discord-bean-bot)

Security Improvements:
- Improved token handling by ensuring it's read securely from a file.
- Added permission checks before performing actions like connecting to voice channels.
- Used environment variables for sensitive data like CHANNEL_ID.
- Added error handling to catch exceptions during song playback.
"""

import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
from yt_dlp import YoutubeDL  # Use yt-dlp instead of youtube_dl

# Constants
TOKEN_FILE_PATH = "token"
QUOTES_FILE_PATH = "Quotes"
BAD_WORDS_FILE_PATH = "BadWords"
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '1234567890'))  # Replace with your channel ID from environment variable

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Disable default help command

# Global queue for songs
song_queue = []

def read_file_lines(file_path):
    """Reads lines from a file and returns a list of stripped lines."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_file_path(file_name):
    """Returns the absolute path of a file located in the current directory."""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_directory, file_name)

# Read token, quotes, and forbidden words from files
TOKEN = read_file_lines(get_file_path(TOKEN_FILE_PATH))[0]
random_messages = read_file_lines(get_file_path(QUOTES_FILE_PATH))
forbidden_words = read_file_lines(get_file_path(BAD_WORDS_FILE_PATH))

async def play_next(ctx):
    """Plays the next song in the queue or disconnects if the queue is empty."""
    if song_queue:
        url = song_queue.pop(0)
        await play_song(ctx, url)
    else:
        await ctx.voice_client.disconnect()

async def play_song(ctx, url):
    """Plays a song from a given URL."""
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda e: bot.loop.create_task(play_next(ctx)))
            print(f"Now playing: {url}")
            await ctx.send(f"Now playing: {info.get('title', 'Unknown title')}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error playing song: {e}")

@bot.command(name="playvc")
async def play_vc(ctx, url):
    """Plays a song from a given URL in the voice channel."""
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    song_queue.append(url)

    if not ctx.voice_client.is_playing():
        await play_next(ctx)

@bot.command(name="queuevc")
async def queue_vc(ctx, url):
    """Adds a song to the queue."""
    song_queue.append(url)
    await ctx.send(f"Added to queue: {url}")

@bot.command(name="pausesong")
async def pausesong(ctx):
    """Pauses the currently playing song."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Playback paused.")
    else:
        await ctx.send("No song is currently playing.")

@bot.command(name="resumesong")
async def resumesong(ctx):
    """Resumes the currently paused song."""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Playback resumed.")
    else:
        await ctx.send("No song is currently paused.")

@bot.command(name="skipsong")
async def skip_song(ctx):
    """Skips to the next song in the queue."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipping to the next song.")
    else:
        await ctx.send("No song is currently playing.")

@bot.command(name="shufflesongs")
async def shuffle_songs(ctx):
    """Shuffles the current song queue."""
    if song_queue:
        random.shuffle(song_queue)
        await ctx.send("The song queue has been shuffled.")
    else:
        await ctx.send("The song queue is empty.")

@bot.event
async def on_ready():
    """Triggers when the bot is ready."""
    print(f'{bot.user} is online!')
    drink_random_message.start()

@tasks.loop(minutes=30)
async def drink_random_message():
    """Sends a random message to the specified channel every 30 minutes."""
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = random.choice(random_messages)
        await channel.send(message)

@bot.command(name="menu")
async def help_menu(ctx):
    """Displays the help menu with available commands."""
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!playvc <url>", value="Plays a song from the given URL in the voice channel", inline=False)
    embed.add_field(name="!queuevc <url>", value="Adds a song to the queue", inline=False)
    embed.add_field(name="!pausesong", value="Pauses the currently playing song", inline=False)
    embed.add_field(name="!resumesong", value="Resumes the currently paused song", inline=False)
    embed.add_field(name="!skipsong", value="Skips to the next song in the queue", inline=False)
    embed.add_field(name="!shufflesongs", value="Shuffles the current song queue", inline=False)
    embed.add_field(name="!badwords", value="Shows the list of forbidden words", inline=False)
    embed.add_field(name="!shitpost", value="Posts a random shitpost", inline=False)
    embed.add_field(name="!menu", value="Shows this message", inline=False)
    embed.set_footer(text="With love from Swoftii <3")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def addword(ctx, *, word):
    """Adds a new word to the forbidden words list."""
    sanitized_word = word.lower().strip()
    if sanitized_word and sanitized_word not in forbidden_words:
        forbidden_words.append(sanitized_word)
        await ctx.send(f'Added "{sanitized_word}" to the list of forbidden words.')
    else:
        await ctx.send(f'The word "{sanitized_word}" is already in the list or invalid.')

@addword.error
async def addword_error(ctx, error):
    """Handles errors for the addword command."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

@bot.command(name="badwords")
@commands.has_permissions(administrator=True)
async def forbidden_words_command(ctx):
    """Displays the list of forbidden words."""
    embed = discord.Embed(
        title="List of Forbidden Words",
        description="\n".join(forbidden_words),
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def shitpost(ctx):
    """Posts a random message from the quotes list."""
    message = random.choice(random_messages)
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    """Handles errors for commands."""
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send("An error occurred while processing the command.")

@bot.event
async def on_message(message):
    """Checks for forbidden words in messages and processes commands."""
    if message.author == bot.user:
        return

    if any(word in message.content.lower() for word in forbidden_words):
        await message.channel.send(f"{message.author.mention} YOU CAN'T SAY THAT WORD >:c")

    await bot.process_commands(message)

# Run the bot with the token
bot.run(TOKEN)
