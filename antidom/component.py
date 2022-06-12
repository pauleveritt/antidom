from typing import Callable, Protocol, Type, TypeVar

from antidote import implements, interface, world, inject

from antidom.resource import Resource
from antidom.viewdom import VDOM


@interface
class Component(Protocol):

    def __vdom__(self) -> VDOM:
        ...


C = TypeVar('C', bound=Type[Component])


def component(context: Type[Resource]) -> Callable[[C], C]:
    def decorate(cls: C) -> C:
        implements(Component).when(qualified_by=context)(cls)
        return cls

    return decorate


def get_component(this_resource: Resource = inject.me()) -> Component:
    """Find the correct component for the context."""
    context_type = this_resource.__class__
    components = world.get[Component]  # type: ignore
    this_component = components.single(qualified_by=context_type)
    return this_component
