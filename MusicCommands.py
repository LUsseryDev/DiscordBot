import asyncio

import discord
from discord.ext import commands

import yt_dlp

ytdlpFormat = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ytdlp = yt_dlp.YoutubeDL(ytdlpFormat)


class MusicCMDs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url:str):

        channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        async with ctx.typing():

            data = await self.bot.loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=False))
            player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(data['url']))
            #ctx.voice_client.play(player)
            ctx.voice_client.play(player, after=lambda e: print(f'PLayer error {e}') if e else None)
        await ctx.send(f'Now playing: {data['title']}')

    @play.error
    async def playError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing url")

    # @commands.command()
    # async def local(self, ctx):
    #     channel = ctx.author.voice.channel
    #
    #     if ctx.voice_client is not None:
    #         await ctx.voice_client.move_to(channel)
    #     else:
    #         await channel.connect()
    #
    #     player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('youtube-LhKJ4lLHBeI-The_Archives.webm'))
    #     player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('https://rr5---sn-5uaeznlz.googlevideo.com/videoplayback?expire=1780491244&ei=jM8favqJMqmylu8PoYbayAg&ip=172.2.16.242&id=o-AKwuqNg0UEQqG9ADFaakSN0hymEE1gRxOCamv1zkvM2o&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&cps=314&met=1780469644%2C&mh=28&mm=31%2C29&mn=sn-5uaeznlz%2Csn-5ualdnzs&ms=au%2Crdu&mv=m&mvi=5&pl=20&rms=au%2Cau&gcr=us&initcwndbps=2555000&bui=AbKmrwqE03JY7uNARIX11bntR_YH-1AU9Il2qSPMJ35ZD21etnbIcGZy33bwzB3fF9Aw48RPhJVirVdy&spc=96Xrv-Ap3J4Xa7jtsLvY8pHY1ZRx4Ek6hcutJX_aJiiB&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2069477&dur=111.501&lmt=1714597324687993&mt=1780469136&fvip=5&keepalive=yes&fexp=51565115%2C51565681&c=ANDROID_VR&txp=2318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cbui%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AHEqNM4wRQIgdgZdoP2xxJqaR_q7boS_SHNqvWc2NISIiURqaG8k98QCIQCVG6xw96Z830nJpHJeYHoQ1BGMABa7IeTbXqBFHxD_bA%3D%3D&lsparams=cps%2Cmet%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=APaTxxMwRgIhAIBII4eRafx5lDoNd0MLp9K0e0_hXV0sB-C3StbWFcZsAiEA75Rb1Tkt2waxUS_fm7xk_5MuekxoFglfXl_dNPbWaIA%3D'))
    #     ctx.voice_client.play(player)



    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()