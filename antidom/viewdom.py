"""ViewDOM."""
from __future__ import annotations

import threading
from collections import ChainMap
from collections.abc import ByteString
from collections.abc import Iterable
from typing import Any, Generator, Literal, Callable, cast
from typing import Mapping
from typing import Optional
from typing import Sequence

from antidote import world

from .htm import htm, VDOMNode, VDOM


def escape(fake: object) -> str:
    # TODO Consider using MarkupSafe for escaping
    return str(fake)


# "void" elements are allowed to be self-closing
# https://html.spec.whatwg.org/multipage/syntax.html#void-elements
VOIDS = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)

html = htm()


def flatten(
        value: Sequence[str | VDOMNode] | VDOMNode | Callable[..., Any]
) -> Generator[VDOMNode | str, Any, Any]:
    """Reduce a sequence."""
    if isinstance(value, Iterable) and not isinstance(
            value, (VDOMNode, str, ByteString)
    ):
        for item in value:
            yield from flatten(item)
    elif callable(value):
        # E.g. a dataclass with an __call__
        vdom = value()
        yield vdom
    else:
        yield value


def relaxed_call(
        callable_: Callable[..., VDOMNode],
        children: list[str | VDOMNode | Sequence[VDOMNode]] | None = None,
        props: Optional[Mapping[str, object]] = None,
) -> VDOM:
    """Very simplified version of ViewDOM instantiation."""
    # Props should include children, which come from "the system"
    if props is None:
        props = {}
    full_props = props | dict(children=children)

    # Get a constructed instance from the Antidote world.
    # TODO Provide the props in some manner.
    # TODO If the world doesn't know about the callable_ because
    #    it isn't registered, it means it is a local symbol. Later,
    #    I'll make some logic to construct simple unregistered components.
    # TODO Fix the typing on this, should be a type, not a Callable
    target = world.get(callable_)  # type: ignore
    if callable(target):
        # This is class-based component. Rendering happens in two steps.
        result: VDOMNode = target()
        return result

    return cast(VDOMNode, target)


def render(value: VDOM) -> str:
    """Render a VDOM to a string."""
    return "".join(
        render_gen(value)
    )


def render_gen(
        value: Sequence[str | VDOMNode] | VDOMNode | Callable[..., Any]
) -> Iterable[str]:
    """Render as a generator."""
    for item in flatten(value):
        if isinstance(item, VDOMNode):
            this_tag, props, children = item.tag, item.props, item.children

            # Is this_tag a callable component, or just '<div>'?
            if callable(this_tag):
                yield from render_gen(
                    relaxed_call(this_tag, props=props)
                )
                continue

            yield f"<{escape(this_tag)}"
            if props:
                pi = props.items()
                yield f" {' '.join(encode_prop(k, v) for (k, v) in pi)}"

            if children:
                yield ">"
                yield from render_gen(children)
                yield f"</{escape(this_tag)}>"
            elif this_tag.lower() in VOIDS:
                yield "/>"
            else:
                yield f"></{this_tag}>"
        elif item not in (True, False, None):  # type: ignore
            yield escape(item)


def encode_prop(k: str, v: object | Literal[True]) -> str:
    """If possible, reduce an attribute to just the name."""
    if v is True:
        return escape(k)
    return f'{escape(k)}="{escape(v)}"'


# #########
# The Context API is currently unused. It will be replaced later
# with a non-threadlocal implementation in the switch to asyncio.


_local = threading.local()


def Context(children: Iterable[VDOMNode] | None = None, **kwargs: Any) -> Generator[
    Iterable[VDOMNode] | None, Any, Any]:  # noqa: N802
    """Like the React Conext API."""
    context: ChainMap[str, object] = getattr(_local, "context", ChainMap())
    try:
        _local.context = context.new_child(kwargs)
        yield children
    finally:
        _local.context = context


def use_context(key: str, default: object = None) -> object:
    """Similar to the React use context API."""
    context: ChainMap[str, object] = getattr(_local, "context", ChainMap())
    return context.get(key, default)
