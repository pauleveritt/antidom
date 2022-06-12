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


@pytest.fixture
def greeter_resource() -> Greeter:
    """Simulate a request which puts a Store in as the resource."""
    greeter = Greeter(name='fixture_greeter', parent=None)
    add_resource(greeter)
    return greeter


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


def test_simple_resource(greeter_resource: Greeter) -> None:
    from antidom.examples.simple_resource import main
    result = render(main())
    assert "Hello fixture_greeter" == result


def test_view_component(store_resource: Store) -> None:
    from antidom.examples.view_component import main
    result = render(main())
    assert "Welcome to Store View" == result
