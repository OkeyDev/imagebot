from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from slowapi.util import get_remote_address
from sqlmodel import Session

from api.config import settings
from api.database.connection import create_db_sessionmaker
from passlib.context import CryptContext

from slowapi import Limiter

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
sessionmaker = create_db_sessionmaker(str(settings.database_url))
limiter = Limiter(key_func=get_remote_address, storage_uri=str(settings.redis_url))


DatabaseDep = Annotated[Session, Depends(sessionmaker)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
