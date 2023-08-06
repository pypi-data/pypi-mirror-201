# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncIterable

import fastapi
from ckms.core import Keychain
from headless.ext.oauth2 import Client
from headless.ext.oauth2.models import ClientAuthenticationMethod

from cbra.core.conf import settings
from cbra.core.params import ApplicationKeychain
from cbra.types import Request


__all__: list[str] = ['ApplicationClient']


def uses_client_secret(method: ClientAuthenticationMethod):
    return method in {
        ClientAuthenticationMethod.client_secret_basic,
        ClientAuthenticationMethod.client_secret_post
    }


def uses_client_jwt_assertion(method: ClientAuthenticationMethod) -> bool:
    return method == ClientAuthenticationMethod.private_key_jwt


async def get(
    request: Request,
    keychain: Keychain = ApplicationKeychain
) -> AsyncIterable[Client]:
    domain: str = request.url.netloc
    client_id: str | None = settings.APP_CLIENT_DOMAINS.get(domain) or settings.APP_CLIENT_ID
    if client_id is None:
        raise ValueError("Configure the APP_CLIENT_ID setting")
    method = ClientAuthenticationMethod(settings.APP_CLIENT_AUTHENTICATION_METHOD)
    params: dict[str, Any] = {
        'issuer': settings.APP_ISSUER,
        'client_auth': method,
        'client_id': client_id,
        'trust_email': settings.APP_ISSUER_TRUST
    }
    if uses_client_secret(method):
        params['client_secret'] = settings.APP_CLIENT_SECRET
    elif uses_client_jwt_assertion(method):
        params.update({
            'signing_key': keychain.get('sig'),
            'encryption_key': keychain.get('enc')
        })
    else:
        raise NotImplementedError
    async with Client(**params) as client:
        yield client


ApplicationClient: Client = fastapi.Depends(get)