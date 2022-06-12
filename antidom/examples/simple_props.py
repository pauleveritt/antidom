"""A stub for the case of passing props to a component."""
from dataclasses import dataclass

from antidote import injectable

from antidom import html, VDOM
from antidom.viewdom import render


@injectable()
@dataclass
class Heading:
    """The default heading."""
    punctuation: str

    def __call__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>My Title{self.punctuation}</h1>")


def main() -> tuple[str, str]:
    actual = render(html('<{Heading} punctuation="!" />'))
    return actual, '<h1>My Title!!</h1>'
