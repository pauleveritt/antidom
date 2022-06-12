"""The simplest template using none of Antidote."""
from antidom import html
from antidom.viewdom import render


def main() -> tuple[str, str]:
    actual = render(html('<p>Hello World</p>'))
    return actual, '<p>Hello World</p>'
