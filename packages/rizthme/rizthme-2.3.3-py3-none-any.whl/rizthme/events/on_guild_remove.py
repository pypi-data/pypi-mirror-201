import discord
from rizthme.models.threads import Player


def init(client: "Client"):

    @client.event
    async def on_guild_remove(guild: discord.Guild):
        """
        When a guild is removed, remove the music players linked to it.

        :param guild: The guild that was removed.
        :type guild: discord.Guild
        """
        client.logger.info(f'{guild.name} has been removed')
        Player.get(guild).delete_thread()
