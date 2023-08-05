from rizthme.setting.config import TOKEN


def init(client: "Client"):

    @client.event
    async def on_disconnect():
        """
        this event run after the server disconnect the client.

        It's used to relogin CLIENT.
        """
        client.logger.info('Client down!')
        await client.login(TOKEN)
        client.logger.info('Client up!')
