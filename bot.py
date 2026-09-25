import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

반복_작업 = {}

허용_사용자_ID = 1298600596269568070


@bot.command()
async def 반복(ctx, 횟수: int, *, 내용: str):
    if ctx.author.id != 허용_사용자_ID:
        return

    횟수 = min(max(횟수, 1), 999999999999999)

    if ctx.channel.id in 반복_작업:
        await ctx.send("이미 반복 중이야!")
        return

    async def 보내기():
        try:
            for _ in range(횟수):
                await ctx.send(내용)
                await asyncio.sleep(0.4)
        except asyncio.CancelledError:
            pass
        finally:
            반복_작업.pop(ctx.channel.id, None)

    반복_작업[ctx.channel.id] = asyncio.create_task(보내기())


@bot.command()
async def 중지(ctx):
    if ctx.author.id != 허용_사용자_ID:
        return

    작업 = 반복_작업.get(ctx.channel.id)

    if 작업 is None:
        await ctx.send("현재 반복 중인 작업이 없어!")
        return

    작업.cancel()
    await ctx.send("🛑 반복 중지!")


bot.run(os.environ["DISCORD_TOKEN"])
