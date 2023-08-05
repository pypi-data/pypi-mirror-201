from typing import List
from threading import Semaphore, Lock
from multipledispatch import dispatch

from rizthme.models.threads import playlist_queue_add, music_queue_add
from rizthme.models.musics import SimpleMusic, Playlist


class MusicQueue(List[SimpleMusic]):

    def __init__(self, semaphore: Semaphore, *args):
        super().__init__(*args)
        self._queue_semaphore = semaphore
        self._is_adding_lock = Lock()

    @dispatch(SimpleMusic)
    def add_music(self, music: SimpleMusic):
        # if the message is a valid song
        if music.is_valid(send_message=True):
            music_queue_add(self, music, self._queue_semaphore, self._is_adding_lock)

    @dispatch(Playlist)
    def add_music(self, playlist: Playlist):
        playlist.send("Loading playlist... (this may take a while)")
        playlist_queue_add(self, playlist, self._queue_semaphore, self._is_adding_lock)
