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
import argparse

__version__ = '1.2.2'
__author__ = 'Oleg Lukianov'

#logging.basicConfig(level=logging.DEBUG, filename="./delete_duplicate_mp3.log")
logging.basicConfig(level=logging.DEBUG)

class DeleteDuplicateMusicTrack:
    """
    Main class
    """
    debug_mode = False
    path_main = ""
    HOSTNAME = socket.gethostname()
    list_track = {}
    list_track_unique = []
    list_path = {}

    def get_all_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        number = 0
        path_main = re.sub('/$', '', self.path_main)

        for root, _, files in os.walk(path_main):
            for fname in files:
                number += 1
                self.list_track[str(number)] = fname
                self.list_path[str(number)] = root
                if self.debug_mode:
                    print(f'File={fname} \t path={root} \t _={_}')
        if self.debug_mode:
            print('\n')

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
        print('\n')

    def compare_with_tracks(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        step = 0
        total = self.compare_with_tracks_count()

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
                print('\n')
            if count > 1:
                step += 1
                print(f'~~~~ Step = {step} of {total} (looking word "{track_unique}") ~~~~')
                self.delete_file(list_track, list_path)

    def compare_with_tracks_count(self):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        logging.debug('Run function = %s', this_function_name)
        total = 0

        for track_unique in self.list_track_unique:
            count = 0

            for key_track in self.list_track:
                if re.search(track_unique, self.list_track[key_track]):
                    count += 1
            if count > 1:
                total += 1

        return total

    def delete_file(self, list_track, list_path):
        """
        Documentation
        """
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        #logging.debug('Run function = %s', this_function_name)
        print('~~~~Choose files to delete~~~~')
        for num in list_track:
            full_path_with_file = f'{list_path[num]}/{list_track[num]}'
            file_size = self.file_size(full_path_with_file)
            print(f'Number={num} \t track: "{list_track[num]}" \t'
                    f'size: {file_size} \t path: "{list_path[num]}"')

        try:
            txt = input("~~~~Insert number for delete file: ")
            number = str(txt)
        except (KeyboardInterrupt, EOFError):
            print('\n')
            print('Exit. User press Ctrl+C (KeyboardInterrupt)')
            os._exit(1)

        for num in number:
            if list_track.get(num):
                full_path_with_file = f'{list_path[num]}/{list_track[num]}'
                print(f'Deleted num={num} \t track: "{list_path[num]}"')
                del list_track[num]
                if os.path.exists(full_path_with_file):
                    os.remove(full_path_with_file)
        print('\n')


    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0


    def file_size(self, file_path):
        """
        this function will return the file size
        """
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return self.convert_bytes(file_info.st_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "-path", "--path", type=str, default="/storage/emulated/0/Download")
    parser.add_argument("-d", "-debug", "--debug", default=False, action="store_true")
    args = parser.parse_args()

    print(f"Arguments count: {len(sys.argv)}")
    print(f'Debug mode = {args.debug}')
    print(f'HOSTNAME = {socket.gethostname()}')
    print(f'path = {args.path}')

    if args.path == "/storage/emulated/0/Download":
        print(f'Need set var "--path", path_main={args.path}')
        os._exit(1)

    parse_music_track = DeleteDuplicateMusicTrack()
    parse_music_track.debug_mode = args.debug
    parse_music_track.path_main = args.path
    try:
        parse_music_track.get_all_tracks()
        parse_music_track.unique_names()
        parse_music_track.compare_with_tracks_count()
        parse_music_track.compare_with_tracks()

        if args.debug:
            print(parse_music_track.list_track)
            print(parse_music_track.list_track_unique)
            print(parse_music_track.list_path)
    except (KeyboardInterrupt, EOFError):
        print('\n')
        print('Exit. User press Ctrl+C (KeyboardInterrupt)')
