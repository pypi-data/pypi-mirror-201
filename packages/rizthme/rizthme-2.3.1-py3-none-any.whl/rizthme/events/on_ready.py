from rizthme.models.threads import Player


def init(client: "Client"):

    @client.event
    async def on_ready():
        """
        this event run after the client is ready, the token is valid.

        warning: this event is not lit "on_connect".
        It's used to set up differents settings and variables.
        """
        # Setup Players Guild's thread
        Player.setup_music_queue(client)
        client.logger.info('Client Ready')
