"""Use a get operator with an attr to reduce the surface area."""
from dataclasses import dataclass

from antidote import injectable, world

from antidom.operator import get


@injectable
class Customer:
    first_name: str = "John"


@injectable
@dataclass
class GreeterFirstName:
    customer_name: str = get(Customer, attr="first_name")


def main() -> tuple[str, str]:
    greeter: GreeterFirstName = world.get(GreeterFirstName)
    actual = greeter.customer_name
    return actual, 'John'
