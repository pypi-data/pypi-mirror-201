import os
import subprocess
import discord


def init(client: "Client"):

    @client.command(["kill"])
    async def kill(message: discord.Message):
        """
        This command is for stop the CLIENT,

        If someone wants to use this command,
        his discord user's id need to be in the hard-coded id list
        :param message: discord.Message
        """
        list_admin = [290227829558345728]
        if message.author.id in list_admin:
            await message.reply("SIR, YES SIR !")

            for voice_client in client.voice_clients:
                await voice_client.disconnect()

            # This is a command to kill the current process.
            # Because discord.py API don't make it after disconnected,
            # I need to kill the current process to stop the program.
            # I know that's not a good solution. Contact tamikata#2214 if you have another solution.
            subprocess.run(f'kill -9 {os.getpid()}', shell=True)
