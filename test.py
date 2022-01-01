import re
import sys
import socket
import argparse

def main():
    n = ['Всё это рейв', 'The Rolling Stones', 'Х_й в пальто', 'Колбаса-любовь', 'Блюз', 'Колбаса-любовь (remix)', 'The Rolling Stones (remix)']
    n.sort()
    r = set(n)

    # for x in n:
    #     print(x)

    # print(n)
    # print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "-path", "--path", type=str, default="/storage/emulated/0/Download")
    parser.add_argument("-d", "-debug", "--debug", default=False, action="store_true")
    args = parser.parse_args()

    if args.debug is True or len(sys.argv) == 1:
        main()
    
        print(f"Arguments count: {len(sys.argv)}")
        print(f'Debug mode = {args.debug}')
        print(f'HOSTNAME = {socket.gethostname()}')
        print(f'path = {args.path}')
