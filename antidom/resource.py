"""Define and fetch resources from a resource tree."""
from __future__ import annotations

from copy import copy
from typing import Protocol

from antidote import world, inject, Provide
from antidote.core import Provider, DependencyValue, Container


class Resource(Protocol):
    """A location-aware node in the resource tree."""
    name: str | None
    parent: Resource | None


@world.provider
class ResourceProvider(Provider[str]):
    _current_resource: Resource | None

    def __init__(self, first_resource: Resource | None = None) -> None:
        super().__init__()
        self._current_resource = first_resource

    def clone(self, keep_singletons_cache: bool) -> ResourceProvider:
        this_copy = None if self._current_resource is None else copy(self._current_resource)
        return ResourceProvider(first_resource=this_copy)

    def exists(self, dependency: object) -> bool:
        return dependency is Resource

    def provide(self, dependency: str, container: Container) -> DependencyValue:
        """Actually get the value."""
        return DependencyValue(self._current_resource)

    def add_resource(self, resource: Resource) -> None:
        self._current_resource = resource


@inject
def add_resource(new_resource: Resource,
                 provider: Provide[ResourceProvider] | None = None,
                 ) -> None:
    assert provider is not None
    provider.add_resource(new_resource)


@inject
def get_resource(this_resource: Resource = inject.me()) -> Resource:
    return this_resource
