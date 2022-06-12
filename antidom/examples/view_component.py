"""A view with a template which uses a component."""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, html, Resource, view
from antidom.component import component
from ..resource import add_resource
from ..view import get_view
from ..viewdom import render


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
        return html(f'<h1>Hello {self.greeter.name}</h1>')


@view(context=Greeter)
@dataclass
class GreeterView:
    """Custom view for a greeter."""

    def __vdom__(self) -> VDOM:
        return html('<{Heading} />')


def main() -> tuple[str, str]:
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    this_view = get_view()
    vdom = this_view.__vdom__()
    actual = render(vdom)
    return actual, '<h1>Hello fixture_greeter</h1>'
