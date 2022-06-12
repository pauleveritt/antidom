"""Test the view protocol and decorator.

This example shows views registered for different context resources.
"""
from dataclasses import dataclass

from antidom import VDOM, Resource, html
from antidom.resource import add_resource
from antidom.view import get_view, view
from antidom.viewdom import render


@dataclass
class Customer:
    name: str | None
    parent: Resource | None


@dataclass
class Store:
    name: str | None
    parent: Resource | None


@view(context=Customer)
@dataclass
class CustomerView:
    name: str = "Customer View"

    def __vdom__(self) -> VDOM:
        return html(f'Hello {self.name}')


@view(context=Store)
@dataclass
class StoreView:
    name: str = 'Store View'

    def __vdom__(self) -> VDOM:
        return html(f'Welcome to {self.name}')


def main() -> tuple[str, str]:
    store = Store(name='fixture_store', parent=None)
    add_resource(store)
    this_view = get_view()
    vdom = this_view.__vdom__()
    actual = render(vdom)
    return actual, 'Welcome to Store View'
