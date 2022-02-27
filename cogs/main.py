import discord
from discord.ext import commands, pages
import validators
from core import pixiv

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", guild_ids=[721216108668911636])
    async def help(self, ctx):
        embed = discord.Embed(title="Help", color=0x0096fa, description="There are no commands! Simply send a pixiv link and I will send the full image.")
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if validators.url(message.content) is True:
            if "pixiv.net" and "artworks" in message.content:
                ctx = await self.bot.get_context(message)
                pixivid = message.content.split("/artworks/")[1]
                json = pixiv.request_hibiapi(pixivid)
                links = pixiv.parse_hibiapi(json)
                mirlinks = []
                for i in links:
                    path = i.split("https://i.pximg.net/")[1]
                    mirimg = "https://pximg.jackli.dev/" + path
                    mirlinks.append(mirimg)
                if len(links) > 1:
                    imgpages = []
                    for count, link in enumerate(mirlinks):
                        imgpages.append(discord.Embed(title=f"Full pixiv Image", color=0x0096fa))
                        imgpages[count].set_image(url=link)
                    paginator = pages.Paginator(pages=imgpages, use_default_buttons=False, timeout=None)
                    paginator.add_button(
                        pages.PaginatorButton("prev", label="<", style=discord.ButtonStyle.red)
                    )
                    paginator.add_button(
                        pages.PaginatorButton(
                            "page_indicator", style=discord.ButtonStyle.gray, disabled=True
                        )
                    )
                    paginator.add_button(
                        pages.PaginatorButton("next", label=">", style=discord.ButtonStyle.green)
                    )
                    await paginator.send(ctx)
                else:
                    embed = discord.Embed(title="Full pixiv Image", color=0x0096fa)
                    embed.set_image(url=mirlinks[0])
                    await message.channel.send(embed=embed, reference=message, mention_author=False)

def setup(bot):
    bot.add_cog(Commands(bot))