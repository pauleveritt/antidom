import pytest
from antidote import world


def test_simple_string() -> None:
    with world.test.new():
        from antidom.examples.simple_string import main
        actual, expected = main()
        assert actual == expected


def test_simple_component() -> None:
    from antidom.examples.simple_component import main
    actual, expected = main()
    assert actual == expected


@pytest.mark.skip(reason="Props not implemented in Antidote")
def test_simple_props() -> None:
    from antidom.examples.simple_props import main
    actual, expected = main()
    assert actual == expected


def test_config_injection() -> None:
    from antidom.examples.config_injection import main
    actual, expected = main()
    assert actual == expected


def test_simple_view() -> None:
    from antidom.examples.simple_view import main
    actual, expected = main()
    assert actual == expected


def test_simple_resource() -> None:
    from antidom.examples.simple_resource import main
    actual, expected = main()
    assert actual == expected


def test_view_component() -> None:
    from antidom.examples.view_component import main
    actual, expected = main()
    assert actual == expected


def test_simple_operator() -> None:
    from antidom.examples.simple_operator import main
    actual, expected = main()
    assert actual, expected


def test_view_component_resource_operator() -> None:
    """View that uses a component which plucks name off resource."""
    from antidom.examples.view_component_resource_operator import main
    actual, expected = main()
    assert actual == expected
