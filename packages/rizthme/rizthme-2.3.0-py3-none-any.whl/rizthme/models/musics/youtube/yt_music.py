import discord
from pytube import YouTube
from typing import Callable
from rizthme.models.musics.simple_music import SimpleMusic


class YTMusic(SimpleMusic):
    """
    Class for handling music from YouTube.
    """

    def __init__(self, client: "Client", url: str | YouTube, channel: discord.TextChannel):
        SimpleMusic.__init__(self, client, url, channel)
        if isinstance(url, str):
            self.ytb: YouTube = YouTube(url)
        else:
            self.ytb: YouTube = url
        self._stream_url: str = self.ytb.streams.filter(only_audio=True).order_by('abr').desc().first().url

    def is_valid(self, send_message: bool = False) -> bool:
        """
        Check if the Music instance is correctly playable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the music is valid and playable
        """
        return self._is_url_valid(send_message) and self._is_valid_stream(send_message)

    def _is_url_valid(self, send_message: bool = False) -> bool:
        """
        Check the user's input url, and check if is it empty
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the original_url isn't empty
        """
        valid: bool = self._url != ""
        if send_message and not valid:
            self.client.logger.warning("!play: Dont valid music")
            self.send("Something's wrong, try to use !play like this: \n !play [YouTube's Link]")
        return valid

    def _is_valid_stream(self, send_message: bool = False) -> bool:
        """
        Check if thlogginge audio stream from PyTube library is correct and usable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the stream is usable
        """
        valid: bool = self._stream_url is not None
        if send_message and not valid:
            self.client.logger.critical("!play: Dont valid music")
            self.send("Something's wrong, YouTube link is unfunctionnal")
        return valid

    def get_title(self) -> str:
        """
        :return: Title of the YouTube's video
        """
        return str(self.ytb.title)

    def get_url(self) -> str:
        """
        :return: user's input URL
        """
        return str(self.ytb.watch_url)

    def get_audio_source(self) -> discord.FFmpegPCMAudio:
        """
        Create a discord.FFmpegPCMAudio from the PyTube.Stream gotten in __init__

        The @before_options is here for reconnected automaticaly the voice_client to the stream
        :return: FFmpegPCMAudio usable like AudioSource for discord.VoiceClient
        """
        before_options = " -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        try:
            return discord.FFmpegPCMAudio(self._stream_url, before_options=before_options)
        except Exception as e:
            self.client.logger.critical(f'When FFmpegPCMAudio created:\n{e}')
            self.send('Error with the YouTube API function')

    def get_duration(self) -> int:
        """
        :return: duration of the YouTube's video in seconds
        """
        return self.ytb.length

    def play(self, voice_client: discord.VoiceClient, after: Callable = None) -> None:
        """
        Play the music with the voice_client
        :param voice_client: discord.VoiceClient, voice_client to play the music
        :param after: Callable, Optional argument for call after the music is played
        """
        voice_client.play(self.get_audio_source(), after=after)

    def stop(self, voice_client: discord.VoiceClient) -> None:
        """
        Stop the music with the voice_client
        :param voice_client: discord.VoiceClient, voice_client to stop the music
        """
        voice_client.stop()
