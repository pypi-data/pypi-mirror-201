from abc import ABC, abstractmethod
from typing import Callable

import discord


class Playable(ABC):
    """
    Abstract class for playable items.
    """

    @abstractmethod
    def is_valid(self, send_message: bool = False) -> bool:
        """
        Checks if the playable item is valid.
        """
        pass

    @abstractmethod
    def play(self, voice_client: discord.VoiceClient, after: Callable = None):
        """
        Plays the playable item.
        """
        pass

    @abstractmethod
    def stop(self, voice_client: discord.VoiceClient):
        """
        Stops the playable item.
        """
        pass

    @abstractmethod
    def get_audio_source(self):
        """
        Returns the audio source of the playable item.
        """
        pass

    @abstractmethod
    def get_duration(self) -> int:
        """
        :return: duration of the music in seconds
        """
        pass
