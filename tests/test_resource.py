from antidote import world

from antidom.examples import Customer
from antidom.resource import Resource, add_resource, get_resource


def test_request_resource() -> None:
    """Simulate different requests with a stateful provider."""
    # We haven't added a resource to the provider yet
    this_resource = world.get[Resource]  # type: ignore
    assert this_resource(Resource) is None

    # Now add the resource
    first_customer = Customer(name='First Customer', parent=None)
    add_resource(first_customer)
    assert get_resource() == first_customer

    # Try a second resource
    second_customer = Customer(name='Second Customer', parent=None)
    add_resource(second_customer)
    assert get_resource() == second_customer
