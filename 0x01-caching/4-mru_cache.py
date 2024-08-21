#!/usr/bin/env python3
"""MRU caching"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    Returns a cached dictionary
    """
    def __init__(self):
        super().__init__()
        self.keys_order = []

    def put(self, key, item):
        """Adds key-value pair to dictionary"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.keys_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = self.keys_order.pop(-1)
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        self.cache_data[key] = item
        self.keys_order.append(key)

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None

        self.keys_order.remove(key)
        self.keys_order.append(key)
        return self.cache_data[key]
