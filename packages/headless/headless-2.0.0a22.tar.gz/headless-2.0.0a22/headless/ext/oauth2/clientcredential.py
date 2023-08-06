# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import secrets
from typing import Any

from ckms.core import KeySpecification
from ckms.jose import PayloadCodec

from headless.types import ICredential
from .models import ClientAuthenticationMethod
from .server import Server


class ClientCredential(ICredential):
    client_id: str
    client_secret: str | None
    confidential: bool
    codec: PayloadCodec
    server: Server
    signing_key: KeySpecification | None = None

    @staticmethod
    def now() -> int:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    def __init__(
        self,
        server: Server,
        client_id: str,
        client_secret: str | None,
        signing_key: None | KeySpecification = None,
        using: ClientAuthenticationMethod | None = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.confidential = bool(signing_key) or bool(client_secret)
        self.server = server
        self.using = using or ClientAuthenticationMethod.none

        if not bool(client_secret) ^ bool(signing_key):
            raise TypeError(
                "Provide either the client_secret or signing_key "
                "parameter."
            )

        # Authentication method is always None if no client_secret
        # was given.
        if client_secret is None:
            self.using = ClientAuthenticationMethod.none

        if signing_key is not None:
            self.using = ClientAuthenticationMethod.private_key_jwt
            self.codec = PayloadCodec(
                signing_keys=[signing_key]
            )

        # Assume client_secret_post when a secret is provided.
        if client_secret is not None and not using:
            self.using = ClientAuthenticationMethod.client_secret_post

    def must_authenticate(self, endpoint: str) -> bool:
        return self.confidential and endpoint in {
            self.server.token_endpoint
        }

    async def preprocess_request( # type: ignore
        self,
        url: str,
        json: dict[str, str] | None,
        data: dict[str, str] | None,
        **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        now = self.now()
        if (data or json) and not bool(json) ^ bool(data):
            raise TypeError("Provide either 'data' or 'json'.")
        params = data or json or {}
        if not self.must_authenticate(url):
            return {**kwargs, 'url': url, 'json': json}
        if self.using == ClientAuthenticationMethod.client_secret_post:
            assert self.client_secret is not None
            assert isinstance(params, dict)
            params.update({
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        elif self.using == ClientAuthenticationMethod.private_key_jwt:
            params.update({
                'client_id': self.client_id,
                'client_assertion': await self.create_assertion(
                    aud=url,
                    exp=now + 60,
                    iat=now,
                    jti=secrets.token_urlsafe(24),
                    iss=self.client_id,
                    nbf=now,
                    sub=self.client_id
                ),
                'client_assertion_type': (
                    'urn:ietf:params:oauth:client-assertion-type:'
                    'jwt-bearer'
                ),
            })
        else:
            raise NotImplementedError
        return {**kwargs, 'url': url, 'json': json, 'data': data}

    async def create_assertion(self, **claims: Any) -> str:
        """Create an assertion to prove the identity of the client."""
        return await self.codec.encode(payload=claims)
