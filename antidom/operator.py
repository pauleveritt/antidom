"""Middleware-style operators for injection helpers."""
from typing import Any

from antidote import lazy, world


@lazy
def get(dependency: type, *, attr: str) -> Any:
    this_dependency = world.get[Any](dependency)  # type: ignore
    return getattr(this_dependency, attr)
