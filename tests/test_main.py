from antidom.viewdom import render


def test_single_renderer():
    """Test just one div."""
    from antidom.single_renderer import main
    vdom = main()
    result = render(vdom)
    assert "<h1>My Title!!</h1>" == result
