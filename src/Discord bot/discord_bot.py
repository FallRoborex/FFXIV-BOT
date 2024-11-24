import os
from discord import Intents, Embed
from discord.ext import commands
from dotenv import load_dotenv
import searching

# Load the Token 
load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))

# Bot Setup
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="%%", intents=intents)


# Function that would start the bot
@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f"{bot.user} is now running!")


@bot.hybrid_command()
async def mount(ctx, name: str):
    search = searching.FFXIVSearch()
    result, image_url = search.search_mount(name)

    embed = Embed(title="Mount Search Results", description=f"Result for {name}", colour=0x3100FA)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def minion(ctx, name: str):
    search = searching.FFXIVSearch()
    result, image_url = search.search_minions(name)

    embed = Embed(title="Minion Search Results", description=f"Result for {name}", colour=0x3100FA)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def title(ctx, name: str):
    search = searching.FFXIVSearch()
    result, image_url = search.search_title(name)

    embed = Embed(title="Title Search Results", description=f"Result for {name}", colour=0x3100FA)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def emote(ctx, name: str):
    search = searching.FFXIVSearch()
    result, image_url = search.search_emote(name)

    embed = Embed(title="Emotes Search Results", description=f"Result for {name}", colour=0x3100FA)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def achievement(ctx, name: str):
    result, image_url = searching.search_for_achievement(name)

    embed = Embed(title="Achievement Search Results", description=f"Result for {name}", colour=0x3100FA)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_image(url=image_url)

    await ctx.send(embed=embed)


def main() -> None:
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()

