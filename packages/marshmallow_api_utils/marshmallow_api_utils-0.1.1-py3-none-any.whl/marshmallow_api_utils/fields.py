from dataclasses import MISSING, field, fields
from typing import Any, Callable, Dict


##############################################################
# These fields exist as helpers to write more clear code.
#
# Allowing us to from:
#   entity_id: UUIDType = field(
#       default=None,
#       metadata=dict(dump_only=True, metadata=dict(help='Unique ID of the entity.'))
#   )
# to
#   entity_id: UUIDType = dump_only_field(help='Unique ID of the entity.')
##############################################################
def required_field(
    default: Any = None,
    default_factory: Callable = MISSING,
    dump_only: bool = False,
    load_only: bool = False,
    help: str = None,
    sortable: bool = True,
    # Marshmallow Schema metadata
    metadata: Dict[str, Any] = None,
    # Marshmallow Schema kwargs
    **schema_kwargs,
):
    if default_factory != MISSING and default is None:
        default = MISSING

    return field(
        default=default,
        default_factory=default_factory,
        metadata=dict(
            **{} if schema_kwargs is None else schema_kwargs,
            required=True,
            dump_only=dump_only,
            load_only=load_only,
            metadata=dict(
                **{} if metadata is None else metadata,
                help=help,
                sortable=sortable,
            ),
        ),
    )


def optional_field(
    default: Any = None,
    default_factory: Callable = MISSING,
    dump_only: bool = False,
    load_only: bool = False,
    help: str = None,
    sortable: bool = True,
    # Marshmallow Schema metadata
    metadata: Dict[str, Any] = None,
    # Marshmallow Schema kwargs
    **schema_kwargs,
):
    if default_factory != MISSING and default is None:
        default = MISSING

    return field(
        default=default,
        default_factory=default_factory,
        metadata=dict(
            **{} if schema_kwargs is None else schema_kwargs,
            required=False,
            dump_only=dump_only,
            load_only=load_only,
            metadata=dict(
                **{} if metadata is None else metadata,
                help=help,
                sortable=sortable,
            ),
        ),
    )


def dump_only_field(
    default: Any = None,
    default_factory: Callable = MISSING,
    help: str = None,
    sortable: bool = True,
    # Marshmallow Schema metadata
    metadata: Dict[str, Any] = None,
    # Marshmallow Schema kwargs
    **schema_kwargs,
):
    return optional_field(
        default=default,
        default_factory=default_factory,
        dump_only=True,
        help=help,
        sortable=sortable,
        metadata=metadata,
        **schema_kwargs,
    )


def get_own_fields(cls, memoize=True):
    '''
        Get's a dataclass's own (uninherited) fields.

        If you expect to call this multiple times you can memoize it,
        in which case it'll be saved as a class var, which will be returned next time it's called.
    '''
    if hasattr(cls, '__uninherited_fields__'):
        return getattr(cls, '__uninherited_fields__')

    inherited_fields = [
        f for base in cls.__bases__
        for f in fields(base)
    ]

    uninherited_fields = [
        f for f in fields(cls)
        if f not in inherited_fields
    ]

    if memoize:
        setattr(cls, '__uninherited_fields__', uninherited_fields)

    return uninherited_fields
