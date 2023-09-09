import re

list_track = {'1': 'test[(1)].txt'}
pattern = ".[a-z0-9]{3}$|^[0-9.]{1,4}"

for key_track in list_track:
    unique_name = re.sub(pattern, '', list_track[key_track])
    print(f'unique_name={unique_name}')
