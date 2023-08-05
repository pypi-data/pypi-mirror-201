import discord
from rizthme.models.threads import Player
from rizthme.models.mode import MODE


def init(client: "Client"):

    @client.command(["loop"])
    async def loop(message: discord.Message):
        """
        Setting up the loop mode to the music player in the guild.
        """
        guild: discord.Guild = message.guild or message.author.guild

        Player.get(guild).set_mode(MODE.LOOP)
        await message.channel.send('Mode: Loop activeted !')
