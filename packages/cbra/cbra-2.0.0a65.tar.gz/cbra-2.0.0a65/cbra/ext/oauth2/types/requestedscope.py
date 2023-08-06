# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Union

import pydantic

from cbra.core.iam.models import Subject
from .emailscope import EmailScope
from .iauthorizationrequest import IAuthorizationRequest
from .iresourceowner import IResourceOwner
from .openidscope import OIDCScope
from .profilescope import ProfileScope
from .subscope import SubScope
from .useragentfingerprintscope import UserAgentFingerprint


class RequestedScope(pydantic.BaseModel):
    __root__: Union[
        EmailScope,
        OIDCScope,
        ProfileScope,
        SubScope,
        UserAgentFingerprint
    ]

    @property
    def name(self) -> str:
        return self.__root__.name

    @pydantic.root_validator(pre=True)
    def preprocess(cls, values: dict[str, Any]) -> dict[str, Any]:
        root: dict[str, Any] | str | None = values.get('__root__')
        if isinstance(root, str):
            values['__root__'] = root = {'name': root}
        return values

    def apply(
        self,
        subject: Subject,
        owner: IResourceOwner,
        claims: dict[str, Any],
        request: IAuthorizationRequest | None = None
    ) -> None:
        return self.__root__.apply(
            subject=subject,
            owner=owner,
            claims=claims,
            request=request
        )
    
    def requires_consent(self) -> bool:
        return self.__root__.requires_consent()