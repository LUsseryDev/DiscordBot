import asyncio
import discord
from discord.ext import commands
import ConfigUtil
import MusicCommands
import GeneralCommands
import logging

async def main():

    # Next Features:
    # Add playlist url support


    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    logHandler = logging.StreamHandler()
    logger.addHandler(logHandler)



    config = ConfigUtil.getConfig()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=config['General']['Prefix'], description="Simple bot for playing music and rolling dice, .help", intents=intents)

    # get all commands and load aliases
    musicCog = MusicCommands.MusicCMDs(bot)
    generalCog = GeneralCommands.GeneralCmds(bot)
    cogs = [musicCog, generalCog] #add any new cogs here

    cmds = []
    for cog in cogs:
        cmds += [c.qualified_name for c in cog.walk_commands()]
    ConfigUtil.EnsureAliases(config, cmds)
    for cog in cogs:
        for cmd in cog.walk_commands():
            astr = config['Aliases'][cmd.qualified_name]
            if astr:
                cmd.aliases = astr.split()
        await bot.add_cog(cog)


    print("Starting bot...")
    try:
        await bot.start(config['General']['Token'])
    finally:
        await bot.change_presence(status=discord.Status.offline)
        await bot.close()

asyncio.run(main())