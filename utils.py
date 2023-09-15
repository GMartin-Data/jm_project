from datetime import datetime


def get_timestamp():
    """Help for file horodating"""
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
