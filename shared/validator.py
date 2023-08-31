import re

VALID_IMAGE_FILE_EXT = ['.jpg', '.jpeg', '.png', '.svg']


def validate_image_name(filename: str) -> bool:
    for ext in VALID_IMAGE_FILE_EXT:
        if filename.endswith(ext):
            return True
    return False
