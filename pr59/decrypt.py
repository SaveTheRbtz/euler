#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from collections import Counter
from itertools import cycle

import logging as log

if __debug__:
    log.basicConfig(level=log.DEBUG)
else:
    log.basicConfig()

def find_space(lst):
    """With high probability finds encryption of space"""
    return Counter(lst).most_common(1)[0][0]

def _decrypt(data, key):
    """
    Decrypts Vigenère cipher in data using key

    https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
    """
    decryption = "".join(chr(a^b) for a,b in zip(data, cycle(key)))
    log.info(decryption)
    return decryption

def decrypt(data, key_len=3):
    """Finds key and decrypts data"""
    key = []
    for i in xrange(0, key_len):
        space = find_space(data[i::key_len])
        key += [ space ^ ord(' ') ]
    return _decrypt(data, key)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", type="string", dest="file", default="cipher1.txt")
    (options, args) = parser.parse_args()

    try:
        with open(options.file) as lines:
            raw_data = [ line for line in lines]
    except EnvironmentError:
        log.critical("Can't open file %(file)s", {'file':options.file})

    data = []
    for line in raw_data:
        # XXX(SaveTheRbtz@): use imap
        data.extend(map(int, (char.strip() for char in line.split(','))))

    print sum(map(ord, decrypt(data)))
