#!/usr/bin/env python3
"""FIFO caching"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
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

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                oldest_key = self.keys_order.pop(0)
                del self.cache_data[oldest_key]
                print(f"DISCARD: {oldest_key}")

        self.cache_data[key] = item
        if key not in self.keys_order:
            self.keys_order.append(key)

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
