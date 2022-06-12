"""Test the view protocol and decorator."""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, Resource, html
from antidom.view import get_view, view
from . import Store
from ..resource import add_resource


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


def main() -> VDOM:
    first_greeter = Greeter(name='first', parent=None)
    add_resource(first_greeter)
    this_view = get_view(Greeter)
    result = this_view.__vdom__()
    return result
