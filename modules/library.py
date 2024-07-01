import csv
import random
from abc import ABC
from pathlib import Path
from typing import List, Dict


class Library(ABC):
    def get_next(self):
        ...

    def get_previous(self):
        ...

    def shuffle(self):
        ...


class LocalLibraryWithFile(Library):
    track_list: List[str] = list()
    track_data: Dict[str, Dict] = dict()
    used: List[str] = list()
    currently_played: str = None

    def set_library(self, library_file):
        self.track_data = self._read_library(library_file)
        self.track_list = list(self.track_data.keys())
        self.shuffle()
        self.get_next()

    def _read_library(self, library_file: Path):
        # filename, anime, artist, title, take
        with open(library_file, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            directory = Path(library_file).parent
            return {
                row['filename']: {'path': directory / row['filename'], 'anime': row['anime'],
                                  'artist': row['artist'], 'title': row['title']}
                for row in reader
            }

    def shuffle(self):
        random.shuffle(self.track_list)
        return self.track_list

    def get_next(self):
        if len(self.track_list) > 0:
            if self.currently_played is not None:
                self.used.append(self.currently_played)
            self.currently_played = self.track_list.pop(0)
        return self.get_currently_played_path()

    def get_previous(self):
        if len(self.used) > 0:
            if self.currently_played is not None:
                self.track_list = [self.currently_played] + self.track_list
            self.currently_played = self.used.pop(-1)
        return self.get_currently_played_path()

    def get_currently_played_path(self):
        return self.track_data[self.currently_played]['path']
