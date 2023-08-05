import asyncio
from abc import ABC, abstractmethod

import discord


class AudioItem(ABC):

    def __init__(self, client, url, channel: discord.TextChannel):
        self.client = client
        self._url = url
        self._channel = channel

    @abstractmethod
    def get_title(self) -> str:
        """
        Get title
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        Get url
        """
        pass

    def send(self, message: str):
        """
        Send message to channel
        """
        asyncio.run_coroutine_threadsafe(self._channel.send(message), self.client.loop)
