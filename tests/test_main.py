from antidom import foo


def test_foo() -> None:
    result = foo()
    assert result == 'bar'
