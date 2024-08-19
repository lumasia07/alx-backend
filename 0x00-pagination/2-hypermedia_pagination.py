#!/usr/bin/env python3
"""Simple pagination"""
import csv
import math
from typing import List, Optional, Dict, Any


def index_range(page: int, page_size: int) -> tuple:
    """Returns a tuple containing start and end index"""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get a page of the large dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []
        return dataset[start_index:end_index]
    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Optional[Any]]:
        """Return hypermedia pagination info"""
        data = self.get_page(page, page_size)
        total_size = len(self.dataset())
        total_pages = math.ceil(total_size / page_size)

        next_page = page + 1 if page < total_size else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
