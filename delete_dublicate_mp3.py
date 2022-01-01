"""
If in dir exist the same music track, script is delete it
"""
import os
import inspect
import types
from typing import cast
import logging
import re
import sys
import socket

__version__ = '1.2.1'
__author__ = 'Oleg Lukianov'

#logging.basicConfig(level=logging.DEBUG, filename="./delete_dublicate_mp3.log")
logging.basicConfig(level=logging.DEBUG)

class ParseMusicTrack:
    """
    Main class
    """
    debug_mode = False
    HOSTNAME = socket.gethostname()
    list_track = {}
    list_track_unique = []
    list_path = {}

    if HOSTNAME == 'LK4H2Q05N':
        path_main = "/Users/iuad15au/Downloads/test2"
    elif HOSTNAME == 'localhost':
        path_main = "/storage/emulated/0/Musik/Ленинград"
    else:
        print(f'Need set var "path_main", you HOSTNAME: {HOSTNAME}')
        os._exit(1)

    def get_all_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        all_name = []
        number = 0
        path_main = self.path_main

        for root, _, files in os.walk(path_main):
            for fname in files:
                number += 1
                all_name.append(fname)
                self.list_track[str(number)] = fname
                self.list_path[str(number)] = root
                if self.debug_mode:
                    print(f'File={fname} \t path={root} \t _={_}')
        if self.debug_mode:
            print('\n')

        return all_name

    def unique_names(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        pattern = ".[a-z0-9]{3}$|^[0-9.]{1,4}"

        for key_track in self.list_track:
            unique_name = re.sub(pattern, '', self.list_track[key_track])
            unique_name = unique_name.strip()
            if unique_name not in self.list_track_unique:
                self.list_track_unique.append(unique_name)
                if self.debug_mode:
                    print(f'unique_name={unique_name}')

    def compare_with_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)

        for track_unique in self.list_track_unique:
            count = 0
            list_track = {}
            list_path = {}
            if self.debug_mode:
                print(f'track_unique = {track_unique}')
            for key_track in self.list_track:
                if self.debug_mode:
                    print(f'key_track = {self.list_track[key_track]}')
                if re.search(track_unique, self.list_track[key_track]):
                    count += 1
                    list_track[str(count)] = self.list_track[key_track]
                    list_path[str(count)] = self.list_path[key_track]
                    if self.debug_mode:
                        print(f'unique={track_unique} \t all={self.list_track[key_track]}')
            if self.debug_mode:
                print(f'Number of coincidence = {count}')
            if count > 1:
                self.delete_file(list_track, list_path)

    @staticmethod
    def delete_file(list_track, list_path):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        print('~~~~Choose files to delete~~~~')
        for num in list_track:
            print(f'Number={num} \t track name: "{list_track[num]}" \t '
                    f'path: "{list_path[num]}/{list_track[num]}"')

        try:
            txt = input("~~~~Insert number for delete file: ")
            number = str(txt)
        except KeyboardInterrupt:
            print('\nExit. User press Ctrl+C (KeyboardInterrupt)')
            os._exit(1)

        for num in number:
            if list_track.get(num):
                full_path_with_file = f'{list_path[num]}/{list_track[num]}'
                print(f'Deleted num={num} \t track name: "{full_path_with_file}"')
                del list_track[num]
                if os.path.exists(full_path_with_file):
                    os.remove(full_path_with_file)

        print('\n')

if __name__ == "__main__":
    COUNT = None
    ARG = None
    DEBUG_MODE = False
    for COUNT, ARG in enumerate(sys.argv):
        if re.search('[Dd][Ee][Bb][Uu][Gg]', ARG):
            DEBUG_MODE = True

    if DEBUG_MODE is True or len(sys.argv) == 1:
        parse_music_track = ParseMusicTrack()
        try:
            parse_music_track.debug_mode = DEBUG_MODE
            parse_music_track.get_all_tracks()
            parse_music_track.unique_names()
            parse_music_track.compare_with_tracks()

            if DEBUG_MODE:
                print('\n')
                print(parse_music_track.list_track)
                print(parse_music_track.list_track_unique)
                print(parse_music_track.list_path)
        except KeyboardInterrupt:
            print('\nExit. User press Ctrl+C (KeyboardInterrupt)')
    else:
        print('Incorrect argument (correct only "debug")')
        print(f"Argument {COUNT:>6}: {ARG}")
        print(f"Arguments count: {len(sys.argv)}")
        print(f'Debug mode = {DEBUG_MODE}')
        print(f'HOSTNAME = {socket.gethostname()}')
