import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
from youtube_dl import YoutubeDL

# Constants
TOKEN_FILE_PATH = "token"
QUOTES_FILE_PATH = "Quotes"
BAD_WORDS_FILE_PATH = "BadWords"
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '1234567890'))  # Replace with your channel ID from environment variable

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Global queue for songs
song_queue = []

def read_file_lines(file_path):
    """Reads lines from a file and returns a list of stripped lines."""
    with open(file_path, 'r') as file:
        return [line.strip() for line.readlines()]

def get_file_path(file_name):
    """Returns the absolute path of a file located in the current directory."""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_directory, file_name)

async def play_next(ctx):
    """Plays the next song in the queue or disconnects if the queue is empty."""
    if song_queue:
        url = song_queue.pop(0)
        await play_song(ctx, url)
    else:
        await ctx.voice_client.disconnect()

async def play_song(ctx, url):
    """Plays a song from a given URL."""
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))

@bot.command(name="playvc")
async def play_vc(ctx, url):
    """Plays a song from a given URL in the voice channel."""
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()

    song_queue.append(url)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)

@bot.command(name="queuevc")
async def queue_vc(ctx, url):
    """Adds a song to the queue."""
    song_queue.append(url)
    await ctx.send(f"Added to queue: {url}")
