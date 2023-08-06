from fastapi import FastAPI

from .Meta import title, description, version, release, uri_prefix
from .Controller import router as cert_controller

# Base router for the API.
router = FastAPI(title=title, description=description, version=version,
                 openapi_url=f'{uri_prefix}/openapi.json',
                 redoc_url=f'{uri_prefix}/redoc',
                 docs_url=f'{uri_prefix}/swagger')

# Add the routes of the cert_controller.
router.include_router(cert_controller,
                      prefix=uri_prefix)
