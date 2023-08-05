import discord

from rizthme.models.threads import Player
from rizthme.models.mode import MODE


def init(client: "Client"):

    @client.command(["shuffle"])
    async def shuffle(message: discord.Message):
        """
        Setting up the shuffle mode to the music player in the guild.
        """
        guild: discord.Guild = message.guild or message.author.guild

        Player.get(guild).set_mode(MODE.SHUFFLE)
        await message.channel.send('Mode: Shuffle activeted !')
