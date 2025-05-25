from typing import BinaryIO
from api.shared.file_types import SupportedFileTypes


start_values = {"PNG": b"\x89\x50\x4e\x47", "JPEG": b"\xff\xd8", "WEBP": b"RIFF"}


def get_image_type(image_io: BinaryIO):
    longest_start_bytes = max(len(i) for i in start_values.values())
    start_bytes = image_io.read(longest_start_bytes)
    image_io.seek(0)

    for file_type, start_bytes in start_values.items():
        if start_bytes.startswith(start_bytes):
            return file_type

    return None


def validate_image_mimetype(mimetype: str):
    if "/" not in mimetype:
        return False

    type_, subtype = mimetype.split("/", 1)
    if type_ != "image":
        return False

    if ";" in subtype:  # Check for parametr
        delimiter_index = subtype.index(";")
        subtype = subtype[:delimiter_index]

    if subtype.upper() not in SupportedFileTypes:
        return False

    return True


def get_image_mimetype(type: SupportedFileTypes):
    return "image/" + type.value.lower()
