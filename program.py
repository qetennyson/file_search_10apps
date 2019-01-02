import os
import collections

SearchResult = collections.namedtuple('SearchResult', 'file, line, text')

def main():
    print_header()
    folder = get_folder_from_user()
    if not folder:
        print("Sorry we can't search that location.")
        return

    text = get_search_txt_from_user()
    if not text:
        print("We can't search for nothing.")
        return

    matches = search_folders(folder, text)
    for match in matches:
        print('-----------MATCH------------')
        print(f'file: {match.file}')
        print(f'line: {match.line}')
        print(f'match: {match.text.strip()}')  # strip removes newline from end of readline
        print()


def print_header():
    print("***************************")
    print("      file search app      ")
    print("***************************")

def get_folder_from_user():
    folder = input("What folder do you want to search? ")
    if not folder or not folder.strip():
        return None

    if not os.path.isdir(folder):
        return None

    return os.path.abspath(folder)

def get_search_txt_from_user():
    text = input("What are you searching for [single phrases only!]? ")
    return text.lower() # Makes searching easier


def search_file(filename, search_text):
    matches = []
    with open(filename, 'r', encoding='utf-8') as fin:

        line_num = 0
        for line in fin:
            line_num += 1
            if line.lower().find(search_text) >= 0:
                m = SearchResult(line=line_num, file=filename, text=line)
                matches.append(m)

    return matches

def search_folders(folder, text):
    print(f"Would search {folder} for {text}")

    all_matches = []
    items = os.listdir(folder)

    for item in items:
        full_item = os.path.join(folder, item)
        if os.path.isdir(full_item):
            # BORN FOR RECURSION - MICHAEL KENNEDY
            matches = search_folders(full_item, text)
            all_matches.extend(matches)
        else:
            matches = search_file(full_item, text)
            all_matches.extend(matches)

    return all_matches
if __name__ == '__main__':
    main()