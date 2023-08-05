from rizthme.models.musics import SimpleMusic
from threading import Semaphore, Lock
from tmktthreader import Threader
from typing import List


@Threader
def music_queue_add(queue: List[SimpleMusic], music, queue_semaphore: Semaphore, is_adding_lock: Lock):
    is_adding_lock.acquire()
    queue.append(music)
    queue_semaphore.release()
    music.send(f'Music: "{music.get_title()}", has been added')
    is_adding_lock.release()
