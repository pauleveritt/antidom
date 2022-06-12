"""Define and fetch resources from a resource tree."""
from __future__ import annotations
from typing import Protocol, Callable, Optional


class Resource(Protocol):
    """A location-aware node in the resource tree."""
    name: str | None
    parent: Resource | None


def current_resource() -> Callable[[Resource | None], Resource | None]:
    cr: Resource | None = None

    def _current_resource(new_resource: Resource | None = None) -> Resource | None:
        nonlocal cr
        if new_resource is not None:
            cr = new_resource
        return cr

    return _current_resource
