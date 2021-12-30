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

__version__ = '1.1.2'
__author__ = 'Oleg Lukianov'

#logging.basicConfig(level=logging.DEBUG, filename="./delete_dublicate_mp3.log")
logging.basicConfig(level=logging.DEBUG)

class ParseMusicTrack:
    """
    Main class
    """
    debug_mode = False
    HOSTNAME = socket.gethostname()

    if HOSTNAME == 'LK4H2Q05N':
        path_main = "/Users/iuad15au/Downloads/test"
    elif HOSTNAME == 'localhost':
        path_main = "/storage/emulated/0/Musik/Ленинград"
    else:
        print(f'Need set var "path_main", you HOSTNAME: {HOSTNAME}')
        os._exit(1)

    def parse_all_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        all_name = []
        path_main = self.path_main

        for root, _, files in os.walk(path_main):
            for fname in files:
                all_name.append(fname)
        #         if self.debug_mode:
        #             print(f'File={fname}')
        # if self.debug_mode:
        #     print('\n')

        return all_name

    def unique_names(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        unique_name_all = []
        all_name = self.parse_all_tracks()
        pattern = ".[a-z0-9]{3}$|^[0-9.]{1,4}"

        for file in all_name:
            unique_name = re.sub(pattern, '', file)
            unique_name = unique_name.strip()
            unique_name_all.append(unique_name)
            if self.debug_mode:
                print(f'File={file} \t\t unique_name={unique_name}')
        if self.debug_mode:
            print('\n')

        return set(unique_name_all)

    def compare_with_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        unique_names = self.unique_names()
        all_name = self.parse_all_tracks()
        for name in unique_names:
            new_list = list(filter(lambda key: name in key, all_name))
            if new_list.__len__() > 1:
                print("n=" + new_list.__str__() + " count: " + new_list.__len__().__str__())


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
            parse_music_track.compare_with_tracks()
        except KeyboardInterrupt:
            print('\nExit. User press Ctrl+C (KeyboardInterrupt)')
    else:
        print('Incorrect argument (correct only "debug")')
        print(f"Argument {COUNT:>6}: {ARG}")
        print(f"Arguments count: {len(sys.argv)}")
        print(f'Debug mode = {DEBUG_MODE}')
        print(f'HOSTNAME = {socket.gethostname()}')
