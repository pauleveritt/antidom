from antidom.examples import Customer
from antidom.resource import current_resource


def test_current_resource() -> None:
    cr = current_resource()
    result = cr(None)
    assert None is result

    # Now set a value
    this_resource = Customer(name='This Customer', parent=None)
    result = cr(this_resource)
    assert this_resource == result

