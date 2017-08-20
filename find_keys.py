
import re
import chardet

KEY_PATTERN = re.compile("[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}")


def read_file(filename):
    with open(filename, 'rb') as f:
        encodings = chardet.detect(f.read())
        print('file', filename, 'detected:', encodings)

    with open(filename, 'r', encoding=encodings['encoding']) as f:
        lines = f.readlines()
        print('file', filename, 'decoded using', encodings['encoding'])
        return lines


def find_keys(filename):
    lines = read_file(filename)
    keys = []
    for line in lines:
        line = line.strip()
        m = KEY_PATTERN.findall(line)
        for key in m:
            keys.append(key)
            print('Key found:', key)
    return keys


if __name__ == '__main__':
    keys = find_keys('keys.txt')
    print(len(keys), 'keys found.')