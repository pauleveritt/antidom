from dataclasses import dataclass

from antidote import injectable

from antidom import html, VDOM


@injectable()
@dataclass
class Heading:
    """The default heading."""
    punctuation: str

    def __call__(self) -> VDOM:
        """Render the component."""
        return html(f"<h1>My Title{self.punctuation}</h1>")


def main() -> VDOM:
    return html('<{Heading} punctuation="!" />')
