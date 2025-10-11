import shutil

def get_free_space_gb_str(path: str) -> str:
    
    # Get disk usage statistics
    disk_stats = shutil.disk_usage(path)

    # Access the 'free' attribute for available space in bytes
    free_bytes = disk_stats.free

    # Convert bytes to a more readable unit, such as gigabytes
    free_gigabytes = free_bytes / (1024**3)

    return (f"Free space on '{path}': {free_gigabytes:.2f} GB")
    """Return a human-readable string of free disk space on the given path."""