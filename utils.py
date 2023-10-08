"""
This module sums up different utilities used in the project,
helping to factorize the code.
"""


from datetime import datetime
import functools
import time


def get_timestamp():
    """Help for file horodating"""
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


def timer(func):
  """Print the runtime of the decorated function"""
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    # Before
    start_time = time.perf_counter()
    # Calling the function and storing value to return
    value = func(*args, **kwargs)
    # After
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f"Finished {func.__name__!r} in {run_time: .4f} seconds.")
    return value
  return wrapper_timer
