"""An injectable which gets a value from configuration."""
from dataclasses import dataclass

from antidote import injectable, const

from antidom import html, VDOM
from antidom.viewdom import render


class Config:
    PUNCTUATION = const("!!")


@injectable()
@dataclass
class Heading:
    """The default heading."""

    punctuation: str = Config.PUNCTUATION

    def __call__(self) -> VDOM:
        return html(f"<h1>My Title{self.punctuation}</h1>")


def main() -> tuple[str, str]:
    actual = render(html("<{Heading} />"))
    return actual, '<h1>My Title!!</h1>'
