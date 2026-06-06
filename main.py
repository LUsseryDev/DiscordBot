import asyncio
import atexit

import discord
from discord.ext import commands

import ConfigManager
import MusicCommands
import logging

async def main():

    logHandler = logging.StreamHandler()

    config = ConfigManager.getConfig()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=config['General']['Prefix'], intents=intents)

    await bot.add_cog(MusicCommands.MusicCMDs(bot))


    print("Starting bot...")
    try:
        await bot.start(config['General']['Token'])
    finally:
        await bot.change_presence(status=discord.Status.offline)
        await bot.close()




asyncio.run(main())

