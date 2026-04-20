import os


def check_data_dir(dir_str: str) -> bool:
    """Ensure output directory exists.

    Returns True if created, False if it already existed.
    """
    try:
        os.makedirs(dir_str)
        return True
    except OSError:
        return False
# End of check_data_dir()


def save_with_unique_filename(file_path: str) -> str:
    """Return a safe filename by adding _01, _02, ... if needed."""
    if not os.path.exists(file_path):
        return file_path

    base, ext = os.path.splitext(file_path)
    counter = 1
    while True:
        new_filename = f"{base}_{counter:02d}{ext}"
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1
# End of save_with_unique_filename()