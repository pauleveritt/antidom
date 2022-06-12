from dataclasses import dataclass

from antidote import injectable

from antidom.viewdom import html
from antidom.htm import VDOM


@injectable()
@dataclass
class Heading:
    """The default heading."""

    def __call__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>My Title!!</h1>")


def main() -> VDOM:
    return html("<{Heading} />")