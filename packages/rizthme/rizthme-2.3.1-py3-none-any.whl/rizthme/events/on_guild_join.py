import discord

from rizthme.models.threads import Player


def init(client: "Client"):

    @client.event
    async def on_guild_join(guild: discord.Guild):
        """
        this event is called when a new guild is joined or created by the CLIENT.

        :param guild: The guild that was joined.
        """
        client.logger.info(f"Joined guild {guild.name}")
        Player(client, guild).start()
