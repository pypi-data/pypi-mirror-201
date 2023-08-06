# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import json
from typing import Any
from typing import TypeVar

from google.cloud.datastore import Client

import cbra.core as cbra
from cbra.types import PersistedModel
from cbra.types import ModelInspector
from cbra.types import ModelMetadata
from cbra.types import IPolymorphicCursor
from .basedatastorerepository import BaseDatastoreRepository
from .polymoprhicdatastorecursor import PolymorphicDatatoreCursor
from .types import IDatastoreKey
from .types import IDatastoreEntity

T = TypeVar('T', bound=PersistedModel)


class PolymorphicDatastoreRepository(BaseDatastoreRepository):
    __module__: str = 'cbra.ext.google'
    inspect: ModelInspector = ModelInspector()

    def __init__(
        self,
        client: Client | Any = cbra.inject('GoogleDatastoreClient')
    ):
        if not isinstance(client, Client):
            raise TypeError(f"Invalid client: {repr(client)}")
        self.client = client

    def model_key(
        self,
        obj: type[PersistedModel] | PersistedModel,
        pk: Any | None = None
    ) -> IDatastoreKey:
        """Return a :class:`cbra.ext.google.types.IDatastoreKey` instance
        based on the primary key of the model.
        """
        field = self.inspect.get_primary_key_field(obj)
        if field is None:
            raise TypeError(f'Model {type(obj).__name__} does not have a primary key.')
        return self.key(self.inspect.get_entity_name(obj), pk or getattr(obj, field.name))

    def model_to_entity(self, obj: PersistedModel) -> IDatastoreEntity:
        """Convert a :class:`cbra.types.PersistedModel` to a valid
        :class:`~cbra.ext.google.types.IDatastoreEntity` implementation.
        """
        pk = self.inspect.get_primary_key_field(obj)
        if pk is None:
            raise TypeError(f'Model {type(obj).__name__} does not have a primary key.')
        key = self.model_key(obj)
        data = obj.json(exclude={pk.name})
        return self.entity_factory(key, _metadata=obj.__metadata__.dict(), **json.loads(data))

    async def auto_increment(self, obj: type[PersistedModel] | PersistedModel) -> int:
        """Return an auto incrementing integer to be used as a technical
        primary key.
        """
        return await self.allocate(self.inspect.get_entity_name(obj))

    async def get(self, cls: type[T], pk: Any) -> None | T:
        """Lookup an entity by its primary key."""
        entity = await self.get_entity_by_key(self.model_key(cls, pk))
        if entity is None:
            return None
        field = self.inspect.get_primary_key_field(cls)
        assert field is not None
        return cls.parse_obj({**dict(entity), field.name: pk})


    async def get_metadata(self, key: IDatastoreKey) -> ModelMetadata | None:
        """Return the metadata for the given key, or ``None`` if there is no
        metadata.
        """
        entity = dict((await self.get_entity_by_key(key)) or {}) # type: ignore
        if entity:
            return ModelMetadata.parse_obj(entity['_metadata'])

    async def list(
        self,
        cls: type[T],
        ordering: list[str] | None = None,
        limit: int = 100,
        token: str | None = None
    ) -> IPolymorphicCursor[T]:
        query = functools.partial(
            self.query(kind=cls.__name__).fetch,
            start_cursor=token,
            limit=limit
        )
        result = await self.run_in_executor(query)
        return PolymorphicDatatoreCursor(cls, [x for x in result], result.next_page_token) # type: ignore

    async def persist(self, obj: T) -> T:
        if not isinstance(obj, PersistedModel):
            raise TypeError(type(obj).__name__)
        entity = self.model_to_entity(obj)
        self.inspect.check_metadata(
            old=await self.get_metadata(entity.key),
            new=obj.__metadata__
        )
        await self.put(entity)
        return obj
