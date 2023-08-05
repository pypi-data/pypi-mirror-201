import discord

from rizthme.models.threads import Player


def init(client: "Client"):

    @client.command(["now", "nowplaying"])
    async def now(message: discord.Message):  # sourcery skip: use-named-expression
        """
        Send to the same textual channel, the current music playing in this Guild

        :param message: discord.Message
        """
        guild: discord.Guild = message.guild or message.author.guild

        info = Player.get(guild).get_now_played()

        if info:
            await message.channel.send(f'titre: {info[0]}.\nLien: {info[1]}')
        else:
            await message.channel.send("I'm not playing song")
