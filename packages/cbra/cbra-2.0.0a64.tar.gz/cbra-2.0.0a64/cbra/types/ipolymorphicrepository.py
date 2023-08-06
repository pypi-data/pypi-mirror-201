# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol
from typing import TypeVar

from .ipolymorphiccursor import IPolymorphicCursor
from .ipolymorphicquery import IPolymorphicQuery
from .persistedmodel import PersistedModel


T = TypeVar('T', bound=PersistedModel)


class IPolymorphicRepository(Protocol):
    __module__: str = 'cbra.types'

    async def auto_increment(self, obj: type[PersistedModel] | PersistedModel) -> int:
        """Return an auto incrementing integer to be used as a technical
        primary key.
        """
        ...

    async def list(
        self,
        cls: type[T],
        ordering: list[str] | None = None,
        limit: int = 100,
        token: str | None = None
    ) -> IPolymorphicCursor[T]:
        ...
    async def query(self, cls: type[T]) -> IPolymorphicQuery[T]: ...
    async def get(self, cls: type[T], pk: Any) -> None | T: ...
    async def persist(self, obj: T) -> T: ...