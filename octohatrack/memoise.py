import os
import sys
import atexit
import json
from functools import wraps

## System Startup tasks
if "--no-cache" not in sys.argv:
  # Always run on start import
  cache_file = "cache_file.json"
  cache = {}

  if os.path.isfile(cache_file):
    with open(cache_file, "r") as f:
      try:
        cache = json.load(f)
      except ValueError:
        pass

  # Always run on exit
  def save_cache():
    with open(cache_file, 'w') as f:
      json.dump(cache, f)

  atexit.register(save_cache)

  def memoise(wrapped):

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
      key = args[0]
      if key not in cache:
        cache[key] = wrapped(*args, **kwargs)
      return cache[key]

    return wrapper

else:
  # Disable memoisation, force all calls to happen regardless
  def memoise(wrapped):

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
      return wrapped(*args, **kwargs)

    return wrapper
