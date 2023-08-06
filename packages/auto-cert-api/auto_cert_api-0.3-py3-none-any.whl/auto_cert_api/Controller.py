import logging
from typing import List

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_200_OK

from .CertbotManager import CertbotManager, AvailableDNSProviders, UnavailableDNSProviders
from .Config import CERTS_LOCATION
router = APIRouter()

_logger = logging.getLogger("api:Controller")

mgr = CertbotManager(CERTS_LOCATION)


@router.get('/certificates')
async def list_certificate() -> PlainTextResponse:
    return PlainTextResponse(mgr.list_certs(), status_code=HTTP_200_OK)


@router.post('/certificates')
async def register_certificate(domains: List[str], email: str, provider: AvailableDNSProviders) \
        -> PlainTextResponse:
    return PlainTextResponse(mgr.register_cert(provider, domains, email), status_code=HTTP_200_OK)


@router.patch('/certificates')
async def renew_certificate(name: str, provider: AvailableDNSProviders, force: bool = False) \
        -> PlainTextResponse:
    return PlainTextResponse(mgr.renew_cert(provider, name, force), status_code=HTTP_200_OK)


@router.delete('/certificates')
async def delete_certificate(name: str) \
        -> PlainTextResponse:

    return PlainTextResponse(mgr.delete_cert(name), status_code=HTTP_200_OK)


@router.get('/plugins/errors')
async def list_plugin_errors_certificate(provider: UnavailableDNSProviders) -> PlainTextResponse:
    return PlainTextResponse("\n".join(mgr.list_plugin_errors(provider)), status_code=HTTP_200_OK)
