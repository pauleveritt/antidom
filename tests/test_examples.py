from antidom.viewdom import render


def test_simple_string() -> None:
    from antidom.examples.simple_string import main
    m = main()
    result = render(m)
    assert "<p>Hello World</p>" == result


def test_simple_component() -> None:
    from antidom.examples.simple_component import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result


# def test_simple_props():
#     from antidom.examples.simple_props import main
#     result = render(main())
#     assert "<h1>My Title!!</h1>" == result


def test_config_injection() -> None:
    from antidom.examples.config_injection import main
    result = render(main())
    assert "<h1>My Title!!</h1>" == result
