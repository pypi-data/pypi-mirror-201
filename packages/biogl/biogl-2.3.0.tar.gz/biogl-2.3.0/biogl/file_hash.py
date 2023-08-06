import hashlib
from operator import methodcaller
from functools import partial
from . import flex_open

def file_hash(*fns, hash_name='md5', buffer_size=65536, decompress=False):
    '''
    :param file_paths: Filename(s) of the file(s) to hash
    :param hash_name: The name of the hash to use, from hashlib (default: md5)
    :type hash_name: str
    :param buffer_size: Read buffer size in bytes (default: 65536)
    :type buffer_size: int
    :param decompress: bool
    '''
    h = methodcaller(hash_name)
    hash = h(hashlib)
    if decompress is True:
        open_func = flex_open
    else:
        open_func = partial(open, mode='rb')
    for fn in fns:
        with open_func(fn) as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                if type(data) == str:
                    data = data.encode('utf-8')
                hash.update(data)

    return hash.hexdigest()