from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from .routes.authentication import router as security_router
from .routes.upload import router as upload_router
from .dependencies import limiter
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler

app = FastAPI()

app.include_router(security_router)
app.include_router(upload_router)

# TODO: Заменить на production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
