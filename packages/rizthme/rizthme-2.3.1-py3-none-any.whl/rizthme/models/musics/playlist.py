from abc import ABC

from typing import Iterable

from rizthme.models.musics.audio_item import AudioItem


class Playlist(AudioItem, ABC):

    def get_list_music(self) -> Iterable["Music"]:
        """
        Get list of music from playlist
        """
        pass
