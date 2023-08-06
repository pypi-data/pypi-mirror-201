import inspect
import deprecation
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


class api_field:
    """
    api_field is a decorator for model no-args methods (including async),
    allowing API users to access certain methods, i.e. implementing computed fields
    """

    def __init__(self, fn):
        if not inspect.isfunction(fn):
            raise RuntimeError("only functions and methods can be decorated with api_field")
        self.fn = fn

    def __set_name__(self, owner, name):
        from .models.fields import ComputedField
        fd = ComputedField(is_async=inspect.iscoroutinefunction(self.fn))
        owner._computed_fields[name] = fd
        setattr(owner, name, self.fn)


@deprecation.deprecated(deprecated_in="0.8.2", removed_in="0.10.0",
                        details="use api_field decorator")
def allow_as_field(fn):
    return api_field(fn)
