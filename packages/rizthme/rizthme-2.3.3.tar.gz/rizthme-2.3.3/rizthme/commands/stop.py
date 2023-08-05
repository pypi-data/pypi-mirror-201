import discord

from rizthme.models.threads import Player


def init(client: "Client"):

    @client.command(["stop"])
    async def stop(message: discord.Message):
        """
        Stop the music of your current Guild
        :param message: discord.Message
        """
        guild = message.guild or message.author.guild

        p = Player.get(guild)
        p.clear_queue()
