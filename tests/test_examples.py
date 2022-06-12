import pytest

from antidom.examples import Store
from antidom.examples.simple_resource import Greeter
from antidom.resource import add_resource
from antidom.viewdom import render


@pytest.fixture
def store_resource() -> Store:
    """Simulate a request which puts a Store in as the resource."""
    store = Store(name='fixture_store', parent=None)
    add_resource(store)
    return store


def test_simple_string() -> None:
    from antidom.examples.simple_string import main
    m = main()
    result = render(m)
    assert "<p>Hello World</p>" == result


def test_simple_component() -> None:
    from antidom.examples.simple_component import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


@pytest.mark.skip(reason="Props not implemented in Antidote")
def test_simple_props() -> None:
    from antidom.examples.simple_props import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


def test_config_injection() -> None:
    from antidom.examples.config_injection import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


def test_simple_view(store_resource: Store) -> None:
    from antidom.examples.simple_view import main
    result = render(main())
    assert "Welcome to Store View" == result


def test_simple_resource() -> None:
    from antidom.examples.simple_resource import main
    result = render(main())
    assert "Hello fixture_greeter" == result


def test_view_component() -> None:
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    from antidom.examples.view_component import main
    result = render(main())
    assert result == "<h1>Hello fixture_greeter</h1>"


def test_operator_get(store_resource: Store) -> None:
    from antidom.examples.simple_operator import main
    greeter = main()
    assert "John" == greeter.customer_name


def test_view_component_resource_operator() -> None:
    """View that uses a component which plucks name off resource."""
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    from antidom.examples.view_component_resource_operator import main
    result = render(main())
    assert "<h1>Operator hello fixture_greeter</h1>" == result
