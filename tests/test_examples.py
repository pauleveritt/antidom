from antidom.viewdom import render


def test_simple_string():
    from antidom.examples.simple_string import main
    result = render(main())
    assert "<p>Hello World</p>" == result


def test_simple_component():
    from antidom.examples.simple_component import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


def test_simple_props():
    from antidom.examples.simple_props import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


def test_config_injection():
    from antidom.examples.config_injection import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result
