"""Very simple usage of a component in a template."""
from dataclasses import dataclass

from antidom import html, VDOM
from antidom.component import component
from antidom.viewdom import render


@component()
@dataclass
class Heading:
    """The default heading."""

    def __vdom__(self) -> VDOM:
        return html(f'<h1>My Title!!</h1>')


def main() -> tuple[str, str]:
    actual = render(html('<{Heading} />'))
    return actual, '<h1>My Title!!</h1>'
