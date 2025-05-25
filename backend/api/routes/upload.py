from os import stat
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)

from api.database.models import User
from api.dependencies import DatabaseDep, TokenDep, limiter
from api.logic import user_logic, exceptions
from api.utils.image_validate import (
    get_image_mimetype,
    get_image_type,
    validate_image_mimetype,
)
from api.workers.tasks import convert_image_task
from api.shared.file_types import SupportedFileTypes

router = APIRouter()


def get_current_user(token: TokenDep, session: DatabaseDep):
    try:
        return user_logic.get_user_by_token(token, session)
    except exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/convert")
@limiter.limit("60/minute")
def upload(
    request: Request,  # Rate limit joke
    image_file: UploadFile,
    convert_to: SupportedFileTypes,
    user: Annotated[User, Depends(get_current_user)],
):
    # Не вижу смысл сохранять все в хранилище и потом ещё выгружать оттуда.
    # Меняем формат изображения и возвращаем результат. Все.
    # Правильно ли это? Не уверен. Но если вдруг надо будет сохранять изображения
    # то лучше будет использовать S3
    supported_mimetypes = " ".join(
        i.value for i in SupportedFileTypes
    )  # Может вынести, чтобы не создавалось при вызове функции? Или я уже заморачиваюсь
    wrong_image_type_exception = HTTPException(
        status.HTTP_400_BAD_REQUEST,
        f"Not supported image type. Supported: {supported_mimetypes}",
    )
    if not image_file.content_type or not validate_image_mimetype(
        image_file.content_type
    ):
        raise wrong_image_type_exception
    image_type = get_image_type(image_file.file)
    if image_type is None:
        raise wrong_image_type_exception

    if image_type == convert_to:
        image_bytes = image_file.file.read()
    else:
        task = convert_image_task.delay(image_file.file.read(), convert_to.value)
        image_bytes = task.get(timeout=10)
    return Response(content=image_bytes, media_type=get_image_mimetype(convert_to))
