#!/usr/bin/env python3
"""LFU Caching"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU Cache System"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.freq = {}
        self.lru = {}
        self.access_count = 0

    def put(self, key, item):
        """Add an item to the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.freq[key] += 1
            self.access_count += 1
            self.lru[key] = self.access_count
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.freq.values())
                lfu_keys = [k for k, v in self.freq.items() if v == min_freq]

                if len(lfu_keys) > 1:
                    lru_key = min(lfu_keys, key=lambda k: self.lru[k])
                else:
                    lru_key = lfu_keys[0]

                del self.cache_data[lru_key]
                del self.freq[lru_key]
                del self.lru[lru_key]
                print(f"DISCARD: {lru_key}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.access_count += 1
            self.lru[key] = self.access_count

    def get(self, key):
        """Retrieve an item from the cache"""
        if key is None or key not in self.cache_data:
            return None

        self.freq[key] += 1
        self.access_count += 1
        self.lru[key] = self.access_count
        return self.cache_data[key]
