# Simple in-memory cache
cache = {}

def store_selection(image_id):
    cache["selected"] = image_id

def get_selection():
    return cache.get("selected")