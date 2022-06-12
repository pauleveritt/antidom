"""Test the component protocol and decorator."""
from dataclasses import dataclass

from antidote import inject

from antidom import VDOM, html, Resource
from antidom.component import component
from . import Store


@component(context=Store)
@dataclass
class Heading:
    """The default heading."""

    store: Resource = inject.me()

    def __vdom__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>Hello {self.store.name}</h1>")


def main() -> VDOM:
    return html("<{Heading} />")
