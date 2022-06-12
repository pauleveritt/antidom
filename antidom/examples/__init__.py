from dataclasses import dataclass

from antidom import Resource
from antidom import html, VDOM
from antidom import view


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
    name: str = "Store View"

    def __vdom__(self) -> VDOM:
        return html(f'Welcome to {self.name}')
