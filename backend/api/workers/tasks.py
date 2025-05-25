import subprocess
import tempfile
from pathlib import Path

from celery import Celery

from api.config import settings
from api.shared.file_types import SupportedFileTypes

app = Celery("tasks", backend=str(settings.redis_url), broker=str(settings.redis_url))


def convert_image(file_path: str, convert_to: SupportedFileTypes):
    original_image_path = Path(file_path)

    converted_file_path = original_image_path.with_suffix(
        "." + convert_to.value.lower()
    )
    subprocess.run(["convert", original_image_path, converted_file_path], check=True)

    return converted_file_path.read_bytes()


@app.task()
def convert_image_task(image: bytes, convert_to_s: str):
    if convert_to_s in SupportedFileTypes:
        convert_to = SupportedFileTypes(convert_to_s)
    else:
        raise ValueError(f"Unsopported filetype: {convert_to_s}")
    with tempfile.NamedTemporaryFile("wb") as file:
        file.write(image)
        converted_file = convert_image(file.name, convert_to)
        return converted_file
