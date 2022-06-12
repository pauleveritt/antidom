from dataclasses import dataclass

from antidote import injectable, const

from antidom.htm import VDOM
from antidom.viewdom import html


class Config:
    PUNCTUATION = const("!!")


@injectable()
@dataclass
class Heading:
    """The default heading."""

    punctuation: str = Config.PUNCTUATION

    def __call__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>My Title{self.punctuation}</h1>")


def main() -> VDOM:
    return html("<{Heading} />")