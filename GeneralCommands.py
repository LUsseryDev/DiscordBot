import re
import logging
import random
from discord.ext import commands
import subprocess
import sys



class GeneralCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, rollstr):
        """Rolls some dice

                Parameters
                ----------
                rollstr: str
                    The dice you want to roll, for example 1d20+20d5-7"""
        total = 0
        results = ''
        sign = '+'
        await ctx.send(f"rolling {rollstr}")
        try:
            async with ctx.typing():
                for e in re.split(r'([.+\-])', rollstr):

                    if 'd' in e:
                        parts = e.split('d')
                        eres = [random.randint(1, int(parts[1])) for _ in range(int(parts[0]))]
                        eres.sort()
                        results += str(eres)
                        if sign == '+':
                            total += sum(eres)
                        else:
                            total -= sum(eres)
                    elif e == '-' or e == '+':
                        sign = e
                    else:
                        if sign == '+':
                            total += int(e)
                        else:
                            total -= int(e)
                        results += f'[{sign}{e}]'

            await ctx.send(f"Results: `{results}`\nSum: `{total}`")
        except Exception as e:
            await ctx.send("Invalid dice")
            logging.debug(f"Invalid dice: {rollstr} \nError: {e}")

    @roll.error
    async def rollError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing dice to roll, such as {self.bot.command_prefix}roll 1d20+5d6-5")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot"""
        #async def func():
        await ctx.send("Shutting down...")

        self.bot.loop.stop()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts the bot"""
        # async def func():
        await ctx.send("restarting...")

        self.bot.loop.stop()

        subprocess.run([sys.executable, "main.py"])





