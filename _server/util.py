
from flask import request


def make_cache_key(*args, **kwargs):
    """  generate cache key for flask cache """
    return request.url
