# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from datetime import datetime
from datetime import timezone

import pydantic


class ManagedGrant(pydantic.BaseModel):
    """A grant received from an external identity
    provider.
    """
    client_id: str
    id: str = pydantic.Field(
        default_factory=lambda: secrets.token_urlsafe(96)
    )
    iss: str
    received: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    refresh_token: str
    scope: set[str] = set()
    sub: str | None = None