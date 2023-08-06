import argparse
from datetime import datetime
import requests

VERSION = "1.0"

def main():
    parser = argparse.ArgumentParser(description='a python cli client for torrents-csv', prog = "pytorrent-csv", epilog = f"Version: {str(VERSION)}")

    parser.add_argument("-q", "--query", help = "Torrent names to search", required = True, type = str)
    parser.add_argument("-n", "--number", help = "The number of results to return (default 10)", default = 10, required = False, type = int)
    parser.add_argument("-p", "--page", help = "Page number to return (default 1)", default = 1, required = False, type = int)

    args = parser.parse_args()

    assert len(args.query) > 3, "\n----\nYour query is too short! It has to be 3 or more characters.\n----"

    returnedjson = requests.get(f"https://torrents-csv.ml/service/search?q={args.query}&size={args.number}&page={args.page}")

    listjson = returnedjson.json()
    listjson.reverse()
    print("\n-------------------------------------")
    for element in listjson:
        if element != "error":
            print(f"Name: {element['name']}")
            size = int(element['size_bytes'])
            if 1048576 > size > 1024:
                size = f"{str(size/1024)[:5]} KB"
            elif 1073741824 > size > 1048576:
                size = f"{str(size/1048576)[:5]} MB"
            elif 1099511627776 > size > 1073741824:
                size = f"{str(size/1073741824)[:5]} GB"
            elif size > 1099511627776:
                size = f"{str(size/1099511627776)[:5]} TB"
            print(f"Size: {str(size)}")
            print(f"Created: {datetime.utcfromtimestamp(element['created_unix']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Seeders: {element['seeders']}")
            print(f"Infohash: {element['infohash']}")
            print("-------------------------------------")
        else:
            print(f"An error has occured: {listjson}")
            print("-------------------------------------")

    print(f"\nQuery: {args.query}")
    print(f"Number of results: {args.number}")
    print(f"Page: {args.page}")

# if __name__ == "__main__":
#     main()
