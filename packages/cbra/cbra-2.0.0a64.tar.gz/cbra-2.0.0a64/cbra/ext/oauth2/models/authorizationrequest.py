# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import os
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar
from typing import Union

import fastapi
import pydantic
from canonical import EmailAddress
from headless.ext.oauth2.models import OIDCToken
from headless.ext.oauth2.types import ResponseMode
from headless.ext.oauth2.types import ResponseType

from cbra.types import IDependant
from cbra.types import Request
from cbra.types import SessionClaims
from cbra.core.iam.models import Subject
from cbra.core.ioc import override
from cbra.core.conf import settings
from .authorizationrequestobject import AuthorizationRequestObject
from .authorizationrequestparameters import AuthorizationRequestParameters
from .authorizationrequestreference import AuthorizationRequestReference
from .authorizationrequestclient import AuthorizationRequestClient
from .resourceowner import ResourceOwner
from ..types import AccessType
from ..types import ClientInfo
from ..types import FatalAuthorizationException
from ..types import FrontendException
from ..types import IAuthorizationServerStorage
from ..types import InvalidResponseTypeRequested
from ..types import ITokenBuilder
from ..types import RedirectURI
from ..types import RequestedScope
from ..types import ResourceOwnerIdentifier
from ..types import MissingResponseType


T = TypeVar('T', bound='BaseAuthorizationRequest')


class BaseAuthorizationRequest(IDependant, pydantic.BaseModel):

    @staticmethod
    def get_issuer(request: Request) -> str:
        return settings.OAUTH2_ISSUER or\
            f'{request.url.scheme}://{request.url.netloc}'

    @staticmethod
    def get_remote_host(request: Request) -> str:
        assert request.client is not None
        return str(request.client.host)

    @classmethod
    def fromrequest(
        cls: type[T],
        client: AuthorizationRequestClient = AuthorizationRequestClient.depends(),
        iss: str = fastapi.Depends(get_issuer),
        remote_host: str = fastapi.Depends(get_remote_host),
        access_type: AccessType = fastapi.Query(
            default=AccessType.online,
            title="Access type",
            description=(
                "Indicates whether your application can refresh access tokens "
                "when the user is not present at the browser. Valid parameter "
                "values are `online`, which is the default value, and `offline`."
            )
        ),
        client_id: str | None = fastapi.Query(
            default=None,
            title="Client ID",
            description="Identifies the client that is requesting authorization."
        ),
        response_type: ResponseType | str | None = fastapi.Query(
            default=None,
            title="Response type",
            description=(
                "Informs the authorization server of the desired response type. "
                "This parameter is required."
            ),
            example="code",
        ),
        redirect_uri: RedirectURI | None = fastapi.Query(
            default=None,
            title="Redirect URI",
            description=(
                "The URL to redirect the client to after completing the "
                "flow. Must be an absolute URI that is served over https, if "
                "not redirecting to `localhost`.\n\n"
                "If `redirect_uri` is omitted, the default redirect URI for "
                "the client specified by `client_id` is used. For clients that "
                "do not have a redirect URI specified, this produces an error "
                "state."
            )
        ),
        scope: str | None = fastapi.Query(
            default=None,
            title="Scope",
            description=(
                "A space-delimited list specifying the requested access scope."
            ),
            max_length=512,
            example="hello.world"
        ),
        state: str | None = fastapi.Query(
            default=None,
            title="State",
            description=(
                "An opaque value used by the client to maintain state between "
                "the request and callback. The authorization server includes "
                "this value when redirecting the user-agent back to the client."
            ),
            max_length=64,
            example=bytes.hex(os.urandom(64))
        ),
        response_mode: ResponseMode | None = fastapi.Query(
            default=None,
            title="Response mode",
            description=(
                "Informs the authorization server of the mechanism to be used "
                "for returning authorization response parameters."
            ),
            example="query"
        ),
        request: str | None = fastapi.Query(
            default=None,
            title="Request",
            description=(
                "A JSON Web Token (JWT) whose JWT Claims Set holds the "
                "JSON-encoded OAuth 2.0 authorization request parameters. "
                "Must not be used in combination with the `request_uri` "
                "parameter, and all other parameters except `client_id` "
                "must be absent.\n\n"
                "Confidential and credentialed clients must first sign "
                "the claims using their private key, and then encrypt the "
                "result with the public keys that are provided by the "
                "authorization server through the `jwks_uri` specified "
                "in its metadata."
            )
        ),
        request_uri: str | None = fastapi.Query(
            default=None,
            title="Request URI",
            description=(
                "References a Pushed Authorization Request (PAR) or a remote "
                "object containing the authorization request.\n\n"
                "If the authorization request was pushed to this authorization "
                "server, then the format of the `request_uri` parameter is "
                "`urn:ietf:params:oauth:request_uri:<reference-value>`. "
                "Otherwise, it is an URI using the `https` scheme. If the "
                "`request_uri` parameter is a remote object, then the external "
                "domain must have been priorly whitelisted by the client."
            )
        ),

        # OpenID parameters
        nonce: str | None = fastapi.Query(
            default=None,
            title="Nonce",
            description=(
                "String value used to associate a Client session with an ID Token, "
                "and to mitigate replay attacks. The value is passed through "
                "unmodified from the Authentication Request to the ID Token. "
                "Sufficient entropy MUST be present in the nonce values used "
                "to prevent attackers from guessing values."
            )
        )
    ) -> T:
        raise NotImplementedError

    @classmethod
    def __inject__(cls: type[T]) -> Callable[..., Awaitable[T] | T]:
        return cls.fromrequest


class AuthorizationRequest(BaseAuthorizationRequest):
    __root__: Union[
        AuthorizationRequestReference,
        AuthorizationRequestObject,

        # This needs to be the last value here because it is responsible
        # for raising the abortable.
        AuthorizationRequestParameters,
    ]

    @classmethod
    @override(BaseAuthorizationRequest.fromrequest) # type: ignore
    def fromrequest(cls: type[T], **kwargs: Any) -> T: # type: ignore
        iss: str = kwargs.pop('iss')
        client: AuthorizationRequestClient = kwargs.pop('client')
        try:
            return cls.parse_obj({
                **copy.deepcopy(kwargs),
                'scope': kwargs.get('scope') or set(),
                'client': client,
                'client_info': client.client_info
            })
        except pydantic.ValidationError as e:
            state: str | None = kwargs.get('state')
            redirect_uri = client.get_redirect_uri(kwargs.get('redirect_uri'))

            assert isinstance(redirect_uri, RedirectURI)
            for error in e.errors():
                loc = (error.get('loc') or (None, None))[-1]
                typ = error.get('type') or 'error'
                if loc == 'response_type' and typ == 'type_error.none.not_allowed':
                    raise MissingResponseType(redirect_uri, iss, state)
                if loc == 'response_type' and typ == 'type_error.enum':
                    raise InvalidResponseTypeRequested(redirect_uri, iss, state)
            raise Exception(e)

    @property
    def auth_time(self) -> int:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        assert self.__root__.auth_time is not None
        return self.__root__.auth_time

    @property
    def client_id(self) -> str:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.client_id

    @property
    def client_info(self) -> ClientInfo:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.client_info

    @property
    def code(self) -> str | None:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return str(self.__root__.code) if self.__root__.code else None

    @property
    def consent(self) -> list[RequestedScope]:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.consent

    @property
    def email(self) -> EmailAddress | None:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.email

    @property
    def email_verified(self) -> bool:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.email_verified or False

    @property
    def id(self) -> str:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        assert self.__root__.id is not None
        return self.__root__.id

    @property
    def id_token(self) -> dict[str, Any]:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.id_token

    @property
    def nonce(self) -> str | None:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.nonce

    @property
    def owner(self) -> ResourceOwnerIdentifier:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        assert self.__root__.owner is not None
        return ResourceOwnerIdentifier(
            client_id=self.__root__.client_id,
            sub=self.__root__.owner
        )

    @property
    def redirect_uri(self) -> str:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.redirect_uri

    @property
    def request_uri(self) -> str:
        return f'urn:ietf:params:oauth:request_uri:{self.id}'

    @property
    def scope(self) -> list[RequestedScope]:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.scope

    @property
    def session_id(self) -> str | None:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.session_id

    @property
    def session(self) -> SessionClaims:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        assert self.__root__.session is not None
        return self.__root__.session

    def authenticate(self, oidc: OIDCToken) -> None:
        """Authenticates the request using the external OIDC token."""
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        if self.is_authenticated():
            raise ValueError("Request is already authenticated")
        assert not self.__root__.downstream
        self.__root__.email = oidc.email
        self.__root__.downstream = oidc

    def as_response(self, client: Any, iss: str) -> fastapi.Response:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.as_response(client, iss)

    def get_authorize_url(self, request: fastapi.Request) -> str:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return (
            f"{request.url_for('oauth2.authorize')}?"
            f"request_uri={self.request_uri}&"
            f"client_id={self.__root__.client_id}"
        )
    
    def has_id_token(self) -> bool:
        return 'openid' in {x.name for x in self.scope}

    def has_owner(self) -> bool:
        """Return a boolean indicating if the request has an owner."""
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.owner is not None

    def has_refresh_token(self) -> bool:
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.access_type == AccessType.offline

    def is_authenticated(self) -> bool:
        """Return a boolean indicating if the authorization request was
        authenticated by a downstream identity provider.
        """
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.downstream is not None
    
    def is_owned_by(self, uid: int) -> bool:
        """Return a boolean indicating if the request is owned by the
        user.
        """
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return self.__root__.owner == uid

    def must_consent(self) -> bool:
        """Return a boolean indicating if the resource owner must consent to
        the scope/claims requested.
        """
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        return bool(self.__root__.consent)

    async def load(
        self,
        client: Any,
        storage: Any,
        session_id: str
    ) -> None:
        """Resolve pushed requests or request references so that :attr:`__root__`
        is always an intance of :class:`AuthorizationRequestParameters`.
        """
        self.__root__ = await self.__root__.load(client, storage, session_id)
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        assert self.__root__.id is not None
        self.__root__.session_id = session_id
        await self.persist(storage)

    async def persist(self, storage: IAuthorizationServerStorage) -> None:
        await storage.persist(self.__root__)

    async def verify(
        self,
        builder: ITokenBuilder,
        request: Request,
        session: SessionClaims,
        client: AuthorizationRequestClient,
        owner: ResourceOwner,
        subject: Subject
    ) -> None:
        """Verifies that all parameters in the request are valid, supported
        and allowed by the client, and allowed by the subject.
        """
        sub = owner.sub
        assert session.auth_time is not None
        assert session.email is not None
        assert isinstance(self.__root__, AuthorizationRequestParameters)
        email = self.email or owner.email or session.email
        email_verified = session.email_verified or self.__root__.email_verified
        if not client.allows_email(email):
            raise FrontendException(
                '/select-email',
                next=self.get_authorize_url(request),
            )
        if not client.can_redirect(self.__root__.redirect_uri):
            raise FatalAuthorizationException(
                "The client does not allow redirection to the given "
                "redirect_uri.",
                status_code=403
            )
        if not client.can_use(self.__root__.scope):
            raise FatalAuthorizationException(
                "The client does not allow use of the given scope.",
                status_code=403
            )

        if self.has_id_token() and self.nonce is None: # is openid
            raise FatalAuthorizationException(
                "The 'nonce' parameter is required for OpenID authorization "
                "requests."
            )

        self.__root__.assign(sub)
        self.__root__.session = session
        self.__root__.auth_time = session.auth_time
        self.__root__.email = email
        self.__root__.email_verified = email_verified
        self.__root__.consent = owner.consent_required(self.scope)

        if self.has_id_token():
            # Create an unsigned ID Token that we can display to the end-user.
            assert self.nonce is not None
            assert owner.ppid.value is not None
            assert self.email is not None
            token = builder.id_token(
                subject=subject,
                ppid=owner.ppid.value,
                nonce=self.nonce,
                scope=self.scope,
                access_token=None,
                auth_time=session.auth_time,
                authorization_code=None,
                request=self,
                owner=owner
            )
            self.__root__.id_token = token.claims