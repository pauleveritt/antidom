from typing import Callable, Protocol, Type, TypeVar

from antidote import implements, interface, world, inject

from antidom.viewdom import VDOM
from antidom.resource import Resource


@interface
class View(Protocol):

    def __vdom__(self) -> VDOM:
        ...


V = TypeVar('V', bound=Type[View])


def view(context: Type[Resource]) -> Callable[[V], V]:
    def decorate(cls: V) -> V:
        implements(View).when(qualified_by=context)(cls)
        return cls

    return decorate


@inject
def get_view(this_resource: Resource = inject.me()) -> View:
    """Find the correct view for the context."""
    context_type = this_resource.__class__
    views = world.get[View]  # type: ignore
    this_view = views.single(qualified_by=context_type)
    return this_view
