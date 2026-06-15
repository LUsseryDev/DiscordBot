import util
import time
from collections import deque
import discord
from discord.ext import commands
import yt_dlp

ytdlpFormat = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'extractor_args': {'generic': {'impersonate': ['Chrome-149']}}
}

ytdlp = yt_dlp.YoutubeDL(ytdlpFormat)


class MusicCMDs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.nowPlaying = {}


    @commands.command()
    async def play(self, ctx, url:str):
        """Plays music (or any other YouTube video) in a voice channel

        Parameters
        ----------
        url: str
            The url of the video you want to play"""

        #make sure author is in voice
        if not ctx.author.voice:
            await ctx.send("You aren't in a voice channel")
            return

        #ensure bot is in voice
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        # function for playing next in queue
        def playNext():
            #reset if queue is empty
            if ctx.guild.id not in self.queues or not self.queues[ctx.guild.id]:
                del self.nowPlaying[ctx.guild.id]
                self.queues.pop(ctx.guild.id, None)
                return

            #otherwise play next song
            self.nowPlaying[ctx.guild.id] = self.queues[ctx.guild.id].popleft()
            player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.nowPlaying[ctx.guild.id]['url']))
            self.nowPlaying[ctx.guild.id]['startTime'] = time.time()
            ctx.voice_client.play(player, after=lambda e: print(f'PLayer error {e}') if e else playNext())

        #if already playing, add to queue, otherwise play now
        if ctx.voice_client.is_playing():
            async with ctx.typing():
                if ctx.guild.id not in self.queues:
                    self.queues[ctx.guild.id] = deque()
                d = await self.bot.loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=False))
                self.queues[ctx.guild.id].append(d)
            await ctx.send(f'Added {d['title']} to the queue')
        else:
            async with ctx.typing():

                data = await self.bot.loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=False))
                self.nowPlaying[ctx.guild.id] = data
                player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(data['url']))
                data['startTime'] = time.time()
                ctx.voice_client.play(player, after=lambda e: print(f'PLayer error {e}') if e else playNext())
            await ctx.send(f'Now playing: {data['title']}')

    @play.error
    async def playError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing url to play")

    @commands.command()
    async def stop(self, ctx):
        """Stops playback and makes the bot leave the voice channel"""
        # make sure author is in voice
        if not ctx.author.voice:
            await ctx.send("You aren't in a voice channel")
            return

        # make sure bot is in voice
        if ctx.voice_client is None:
            await ctx.send(f"{self.bot.user.name} isn't in a voice channel")
            return


        await ctx.voice_client.disconnect()
        del self.nowPlaying[ctx.guild.id]
        del self.queues[ctx.guild.id]

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song"""
        # make sure author is in voice
        if not ctx.author.voice:
            await ctx.send("You aren't in a voice channel")
            return

        # make sure bot is in voice
        if ctx.voice_client is None:
            await ctx.send(f"{self.bot.user.name} isn't in a voice channel")
            return

        ctx.voice_client.stop()

    @commands.command()
    async def queue(self, ctx):
        """Shows the song currently playing and any songs in queue"""
        # make sure bot is in voice
        if ctx.voice_client is None:
            await ctx.send(f"{self.bot.user.name} isn't in a voice channel")
            return

        if ctx.guild.id not in self.nowPlaying:
            await ctx.send("Nothing playing")

        currentTime = round(time.time() - self.nowPlaying[ctx.guild.id]['startTime'])
        await ctx.send(f'Now Playing: [{self.nowPlaying[ctx.guild.id]['title']}](<{self.nowPlaying[ctx.guild.id]['original_url']}>)\n'
                       f'[{util.formatTime(currentTime)}/{util.formatTime(self.nowPlaying[ctx.guild.id]['duration'])}]{util.progressBar(currentTime / self.nowPlaying[ctx.guild.id]['duration'], 27)}')

        #make queue show as well as now playing
        if ctx.guild.id not in self.queues:
            return
        qstr = ""
        for i, s in enumerate(self.queues[ctx.guild.id]):
            qstr += f'{i}. [{s['title']}](<{s['original_url']}>)\n'

        await ctx.send(qstr)

    @commands.command()
    async def remove(self, ctx, idx):
        """Remove a song from queue

                Parameters
                ----------
                idx: int
                    The position in queue of the song you want to remove"""
        # make sure author is in voice
        if not ctx.author.voice:
            await ctx.send("You aren't in a voice channel")
            return

        # make sure bot is in voice
        if ctx.voice_client is None:
            await ctx.send(f"{self.bot.user.name} isn't in a voice channel")
            return

        try:
            idx = int(idx)-1
        except ValueError:
            await ctx.send("Invalid index")
            return

        if 0 > idx or idx > len(self.queues[ctx.guild.id]):
            await ctx.send(f"There is no song at position {idx} in the queue")
        s = self.queues[ctx.guild.id][idx]
        del self.queues[ctx.guild.id][idx]
        await ctx.send(f"Removed [{s['title']}](<{s['original_url']}>) from the queue")

    @remove.error
    async def removeError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing position in queue to remove")