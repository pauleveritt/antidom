"""A view which gets the current resource.

This uses a stateful provider. The idea is, on each "request", the value
in the provider is updated.

A temporary workaround until AEP2 lands.
"""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, Resource, html
from antidom.view import get_view, view
from ..resource import add_resource
from ..viewdom import render


@dataclass
class Store:
    name: str | None
    parent: Resource | None


@dataclass
class Greeter:
    name: str | None
    parent: Resource | None


@view(context=Greeter)
@dataclass
class GreeterView:
    """Custom view for a greeter."""
    greeter: Resource = inject.me()

    def __vdom__(self) -> VDOM:
        return html(f'Hello {self.greeter.name}')


def main() -> tuple[str, str]:
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    this_view = get_view()
    vdom = this_view.__vdom__()
    actual = render(vdom)
    return actual, 'Hello fixture_greeter'
