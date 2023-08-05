import discord
import pytube

from pytube.helpers import DeferredGeneratorList
from rizthme.models.musics.playlist import Playlist

from rizthme.models.musics.youtube.yt_music import YTMusic


class YTPlaylist(Playlist):

    def __init__(self, url: str, channel: discord.TextChannel):
        Playlist.__init__(self, url, channel)
        self.plt: pytube.Playlist = pytube.Playlist(url)
        self._title = self.plt.title

    def get_url(self) -> str:
        """
        :return: the url of the playlist
        """
        return self._url

    def _music_generator(self) -> str:
        """
        Generator that yield the music of the playlist
        :return: a music of the playlist
        """
        for youtube in self.plt.videos:
            yield YTMusic(youtube, self._channel)

    def get_list_music(self) -> DeferredGeneratorList:
        """
        :return: the list of music in the playlist
        """
        return DeferredGeneratorList(self._music_generator())

    def get_title(self) -> str:
        """
        :return: the title of the playlist
        """
        return self._title
