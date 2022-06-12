"""Test the view protocol and decorator."""
from dataclasses import dataclass

from antidom import html, VDOM
from antidom.view import view, View, get_view


@dataclass
class Customer:
    name: str


@dataclass
class Store:
    name: str


@view(context=Customer)
@dataclass
class CustomerView:
    name: str = "Customer View"

    def __vdom__(self) -> VDOM:
        return html(f'Hello {self.name}')


@view(context=Store)
@dataclass
class StoreView:
    name: str = "Store View"

    def __vdom__(self) -> VDOM:
        return html(f'Welcome to {self.name}')


def main() -> VDOM:
    this_view = get_view(Store)
    result = this_view.__vdom__()
    return result
