#!/usr/bin/env python3
"""Basic dictionary"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Returns a basic cache dictionary"""

    def put(self, key, item):
        """
        Adds key-value pair to cache_data dict
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves value asscociated with key in cached_data
        """
        if key is not None or key not in self.cache_data:
            return None
        return self.cache_data[key]
