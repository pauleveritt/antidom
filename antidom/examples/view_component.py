"""Test the component protocol and decorator."""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, html, Resource, view
from antidom.component import component
from ..resource import add_resource
from ..view import get_view


@dataclass
class Greeter:
    name: str | None
    parent: Resource | None


@component(context=Greeter)
@dataclass
class Heading:
    """The default heading."""

    greeter: Resource = inject.me()

    def __vdom__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>Hello {self.greeter.name}</h1>")


@view(context=Greeter)
@dataclass
class GreeterView:
    """Custom view for a greeter."""

    def __vdom__(self) -> VDOM:
        return html("<{Heading} />")


def main() -> VDOM:
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    this_view = get_view()
    result = this_view.__vdom__()
    return result
