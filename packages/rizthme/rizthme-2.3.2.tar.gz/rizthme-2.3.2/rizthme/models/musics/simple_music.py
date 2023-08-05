from abc import ABC

from rizthme.models.musics import Playable, AudioItem


class SimpleMusic(AudioItem, Playable, ABC):
    """
    Abstract class for simple music.
    """
    pass
