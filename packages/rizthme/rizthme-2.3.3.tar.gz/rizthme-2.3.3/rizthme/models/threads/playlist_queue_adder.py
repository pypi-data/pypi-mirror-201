from rizthme.models.musics import Playlist, SimpleMusic
from threading import Semaphore, Lock
from tmktthreader import Threader
from typing import List


@Threader
def playlist_queue_add(queue: List[SimpleMusic], playlist: Playlist, queue_semaphore: Semaphore, is_adding_lock: Lock):
    is_adding_lock.acquire()
    # Add all music from the playlist to the queue
    for music in playlist.get_list_music():  # get_list_music() return a DeferredGeneratorList.
        # If the playable is valid, so it can be added to the queue.
        if music.is_valid(send_message=True):
            queue.append(music)
            queue_semaphore.release()
    playlist.send(f"Playlist: {playlist.get_title()} has been added")
    is_adding_lock.release()
