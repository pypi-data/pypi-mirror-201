from dataclasses import asdict, fields
from typing import Any, ClassVar, Dict, Type, TypeVar

import marshmallow as ma
from marshmallow_dataclass import dataclass as ma_dataclass

# Adds type hinting for abstract functions. https://peps.python.org/pep-0673/
SelfMaDataclass = TypeVar("SelfMaDataclass", bound="MaDataclass")


@ma_dataclass
class MaDataclass:
    '''
        Simple base class to add Schema typing and convenience functions for serialization

        Makes it a litte easier to use than having to keep calling the Schema itself.

        To use, extend this class with your class and use it.

        Example:
        ```python
        @ma_dataclass
        class MyMessage(MaDataclass):
            foo: str
            bar: int

        msg = MyMessage(foo='hello', bar=3)
        serialized = msg.dump()
        deserialized = MyMessage.load(serialized)
    '''
    Schema: ClassVar[Type[ma.Schema]] = ma.Schema

    @classmethod
    def load(
        cls: Type[SelfMaDataclass],
        data: Any,
        schema_kwargs: Dict[str, Any] = None,
        **load_kwargs: Dict[str, Any],
    ) -> SelfMaDataclass:
        if schema_kwargs is None:
            schema_kwargs = {}
        return cls.Schema(**schema_kwargs).load(data, **load_kwargs)

    @classmethod
    def loads(
        cls: Type[SelfMaDataclass],
        data: str,
        schema_kwargs: Dict[str, Any] = None,
        **load_kwargs: Dict[str, Any],
    ) -> SelfMaDataclass:
        if schema_kwargs is None:
            schema_kwargs = {}
        return cls.Schema(**schema_kwargs).loads(data, **load_kwargs)

    def dump(
        self: SelfMaDataclass,
        schema_kwargs: Dict[str, Any] = None,
        **dump_kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        if schema_kwargs is None:
            schema_kwargs = {}
        return self.Schema(**schema_kwargs).dump(self, **dump_kwargs)

    def dumps(
        self: SelfMaDataclass,
        schema_kwargs: Dict[str, Any] = None,
        **dump_kwargs: Dict[str, Any],
    ) -> str:
        if schema_kwargs is None:
            schema_kwargs = {}
        return self.Schema(**schema_kwargs).dumps(self, **dump_kwargs)

    def asdict(
        self: SelfMaDataclass,
        include_dump_only_fields: bool = True,
    ) -> Dict[str, Any]:
        '''
            include_dump_only_fields: Will include or exclude all fields marked with 'dump_only=True'
        '''
        result = asdict(self)

        if not include_dump_only_fields:
            for f in fields(self):
                if f.metadata.get('dump_only', False):
                    result.pop(f.name, None)

        return result
