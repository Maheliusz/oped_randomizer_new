import random
from pathlib import Path
import vlc


class LocalPlayer:
    player: vlc.MediaPlayer = vlc.MediaPlayer()
    path: Path = None

    def set_track(self, path):
        self.path = path
        self.player.set_media(vlc.Media(self.path))

    def play(self, from_start=True):
        if self.player.get_media() is not None:
            self.player.play()
            if not from_start:
                while not self.player.is_playing():
                    pass
                length = self.player.get_length()
                random_time = random.randint(0, max(0, length))
                self.set_time_ms(random_time)

    def pause_unpause(self):
        if self.player.get_media() is not None:
            self.player.pause()

    def set_time_seconds(self, time):
        time_ms = time * 1000
        self.set_time_ms(time_ms)

    def set_time_ms(self, time_ms):
        self.player.set_time(time_ms)

    def random_start(self, duration=0):
        duration_ms = duration * 1000
        if self.player.get_media() is not None:
            length = self.player.get_length()
            end = length - duration_ms
            random_time = random.randint(0, max(0, end))
            self.set_time_ms(random_time)
