"""Cache file functions"""

import os
import appdirs
import json
import logging

def get_cache_path():
    """Get cache file path in user's home directory

    :return: cache path
    :rtype: str
    """

    # cache file in user's home directory
    cache_dir = appdirs.user_cache_dir("cryptoprice")
    cache_file = os.path.join(cache_dir, "cryptoprice.cache")

    return cache_file

def read_cache(entry=None):
    """Read cache entry

    :param entry: cache entry to read
    :type entry: hashable
    :return: cache entry
    :rtype: dict
    :raises NoCacheException: if cache file does not exist
    :raises InvalidCacheException: if cache is empty or invalid
    """

    logging.getLogger("cache").debug("Reading cache entry %s", entry)

    cache_path = get_cache_path()

    # cache path must be available
    if cache_path is None:
        raise CacheException()

    # cache path must exist
    if not os.path.isfile(cache_path):
        raise NoCacheException()

    with open(cache_path, "r") as f:
        try:
            cache_dict = json.loads(f.read())
        except json.JSONDecodeError as e:
            # empty or corrupt
            raise InvalidCacheException()

    if entry is not None:
        return cache_dict[entry]

    return cache_dict

def write_cache(new_dict, entry):
    """Write cache entry

    :param new_dict: new dict to cache
    :type new_dict: dict
    :param entry: dict key to write new dict under
    :type entry: hashable
    """

    cache_path = get_cache_path()

    # cache path must be available
    if cache_path is None:
        raise CacheException()

    logging.getLogger("cache").debug("Writing cache entry %s at %s",
                                     entry, cache_path)

    if os.path.isfile(cache_path):
        # update existing cache
        cache_dict = read_cache()
    else:
        logging.getLogger("cache").info("Creating new cache file")

        # create new cache
        cache_dict = {}

        # build cache directory
        directory = os.path.dirname(cache_path)

        # create cache directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    if entry is not None:
        cache_dict[entry] = new_dict
    else:
        cache_dict = new_dict

    with open(cache_path, "w+") as f:
        json.dump(cache_dict, f)

def delete_cache():
    """Delete cache file"""

    cache_path = get_cache_path()

    # delete cache file if it exists
    if os.path.exists(cache_path):
        logging.getLogger("cache").info("Deleting cache file at %s", cache_path)

        os.remove(cache_path)
    else:
        logging.getLogger("cache").debug("No cache file to delete")

class NoCacheException(Exception):
    pass

class InvalidCacheException(Exception):
    pass
