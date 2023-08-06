# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from cbra.core.iam.models import Subject
from .iauthorizationrequest import IAuthorizationRequest
from .iresourceowner import IResourceOwner


class BaseScope(pydantic.BaseModel):
    name: str

    def apply(
        self,
        subject: Subject,
        owner: IResourceOwner,
        claims: dict[str, Any],
        request: IAuthorizationRequest | None = None
    ) -> None:
        raise NotImplementedError

    def requires_consent(self) -> bool:
        return True