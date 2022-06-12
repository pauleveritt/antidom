"""A view which uses a component which plucks the name off a resource."""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, html, Resource, view
from antidom.component import component
from antidom.operator import get


@dataclass
class Greeter:
    name: str | None
    parent: Resource | None


@component(context=Greeter)
@dataclass
class Heading:
    """The default heading."""

    greeter_name: str = get(Resource, attr="name")

    def __vdom__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>Operator hello {self.greeter_name}</h1>")


@view(context=Greeter)
@dataclass
class GreeterView:
    """Custom view for a greeter."""

    def __vdom__(self) -> VDOM:
        return html("<{Heading} />")


def main() -> VDOM:
    return html("<{Heading} />")
