import re
from typing import Optional

import discord

from abc import ABC

from rizthme.exception import BadLinkError
from rizthme.models.musics import YTMusic, YTPlaylist, Playable


class AudioFactory(ABC):
    """
    Factory class for creating music objects.
    """

    client: Optional["Client"] = None

    dict_regex = {
        YTMusic: r"^https?:\/\/(www.)?(youtube.com|youtu.be)\/watch?(.*)$",
        YTPlaylist: r"^https?:\/\/(www.)?(youtube.com|youtu.be)\/playlist?(.*)$",
    }

    def __init__(self):
        raise NotImplementedError("This is an abstract class")

    @classmethod
    def create_playable(cls, message: discord.Message) -> Playable:
        """
        Create a music object based on the message.

        That will check by a regex if the message is a valid link.

        the @dict_regex while be used to have the regex for a specific type of music.
        """
        url = message.content.split(" ")[-1]
        channel = message.channel
        for PlayableClass, regex in cls.dict_regex.items():
            if re.match(regex, url):
                return PlayableClass(cls.client, url, channel)
        raise BadLinkError(f'your URL "{url}" is not a valid link.')
