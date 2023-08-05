from typing import Callable, Any, List
from functools import wraps

from .types import KwArgs
from .errors import ObjectSaveRequired


def save_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    save_required decorator is meant to decorate model methods that
    require a model instance to be saved first.

    For example, StorableModel's own db_update method makes no sense
    until the instance is persisted in the database
    """
    @wraps(func)
    def wrapper(self, *args: List[Any], **kwargs: KwArgs) -> Any:
        if self.is_new:
            raise ObjectSaveRequired("This object must be saved first")
        return func(*args, **kwargs)

    return wrapper


class allow_as_field:
    """
    allow_as_field decorator copies async methods essentially
    adding _allowed_as_field to their names. This protects models asynchronous
    methods from being accessed via api by their names listed in _fields
    param as only methods with _allowed_as_field suffix will be processed

    """
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        original_name = self.fn.__name__
        allowed_method_name = f"{self.fn.__name__}_allowed_as_field"
        setattr(owner, allowed_method_name, self.fn)
        setattr(owner, original_name, self.fn)
        return self.fn
