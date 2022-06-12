from typing import cast

from antidote import world

from antidom.examples import Customer
from antidom.resource import Resource, add_resource


# def test_current_resource() -> None:
#     cr = current_resource()
#     result = cr(None)
#     assert None is result
#
#     # Now set a value
#     this_resource = Customer(name='This Customer', parent=None)
#     result = cr(this_resource)
#     assert this_resource == result


def test_get_resource() -> None:
    # We haven't added a resource to the provider yet
    this_customer = Customer(name='First Customer', parent=None)
    this_resource = world.get[Resource]  # type: ignore
    assert this_resource(Resource) is None

    # Now add the resource
    add_resource(this_customer)
    this_resource = world.get[Resource]  # type: ignore
    assert this_resource(Resource) == this_customer
