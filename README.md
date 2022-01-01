1. Install all requirements on host
pip3 install -r requirements.txt

2. Create requirements file
pip3 freeze > requirements.txt

## Using
$ python3 delete_duplicate_mp3.py --help
$ python3 delete_duplicate_mp3.py --path "/storage/emulated/0/Musik/Ленинград"
$ python3 delete_duplicate_mp3.py --debug --path "/storage/emulated/0/Musik/Ленинград"
