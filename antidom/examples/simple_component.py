from dataclasses import dataclass

from antidom import html, VDOM
from antidom.component import component


@component()
@dataclass
class Heading:
    """The default heading."""

    def __vdom__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>My Title!!</h1>")


def main() -> VDOM:
    return html("<{Heading} />")
