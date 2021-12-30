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

__version__ = '1.1.1'
__author__ = 'Oleg Lukianov'

#logging.basicConfig(level=logging.DEBUG, filename="./delete_dublicate_mp3.log")
logging.basicConfig(level=logging.DEBUG)

class ParseMusicTrack:
    path_main = "/Users/iuad15au/Downloads/test"
    debug_mode = False

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
                    path = os.path.join(root, fname)
                    all_name.append(fname)
                    if self.debug_mode:
                        print(f'File={fname}')
            if self.debug_mode:
                print('\n')

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

            return unique_name_all

    def compare_with_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        unique_names = self.unique_names()
        all_name = self.parse_all_tracks()
        for unique_name in unique_names:
            newList = list(filter(lambda key: unique_name in key, all_name))
            if newList.__len__() > 1:
                #print(f'yes - x={unique_name}')
                print("n=" + newList.__str__() + " count: " + newList.__len__().__str__())
            # else:
            #     print(f'no  - x={unique_name}')
            #     print("n=" + newList.__str__() + " count: " + newList.__len__().__str__())


if __name__ == "__main__":
    COUNT = None
    ARG = None
    debug_mode = False
    for COUNT, ARG in enumerate(sys.argv):
        if re.search('[Dd][Ee][Bb][Uu][Gg]', ARG):
            debug_mode = True

    if debug_mode is True or len(sys.argv) == 1:
        parse_music_track = ParseMusicTrack()
        try:
            parse_music_track.debug_mode = debug_mode
            parse_music_track.compare_with_tracks()
        except KeyboardInterrupt:
            print('\nExit. User press Ctrl+C (KeyboardInterrupt)')
    else:
        print('Incorrect argument (correct only "debug")')
        print(f"Argument {COUNT:>6}: {ARG}")
        print(f"Arguments count: {len(sys.argv)}")
        print(f'Debug mode = {debug_mode}')