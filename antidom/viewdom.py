"""ViewDOM."""
from __future__ import annotations

import threading
from collections import ChainMap
from collections.abc import ByteString
from collections.abc import Iterable
from dataclasses import dataclass
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union

from antidote import world

from .htm import htm


def escape(fake):
    # TODO Consider using MarkupSafe for escaping
    return fake


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


@dataclass(frozen=True)
class VDOMNode:
    """Implementation of a node with three slots."""

    __slots__ = ["tag", "props", "children"]
    tag: str
    props: Mapping
    children: List[Union[str, VDOMNode]]


VDOM = Union[Sequence[VDOMNode], VDOMNode]

html = htm(VDOMNode)


def flatten(value):
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
        callable_,
        children=None,
        props: Optional[Mapping] = None,
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
    target = world.get(callable_)
    if callable(target):
        # This is class-based component. Rendering happens in two steps.
        return target()

    return target


def render(value: VDOM) -> str:
    """Render a VDOM to a string."""
    return "".join(
        render_gen(
            value,
            children=None,
        )
    )


def render_gen(value, children=None):
    """Render as a generator."""
    for item in flatten(value):
        if isinstance(item, VDOMNode):
            this_tag, props, children = item.tag, item.props, item.children

            # Is this_tag a callable component, or just '<div>'?
            if callable(this_tag):
                yield from render_gen(
                    relaxed_call(this_tag, children=children, props=props)
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
        elif item not in (True, False, None):
            yield escape(item)


def encode_prop(k, v):
    """If possible, reduce an attribute to just the name."""
    if v is True:
        return escape(k)
    return f'{escape(k)}="{escape(v)}"'


# #########
# The Context API is currently unused. It will be replaced later
# with a non-threadlocal implementation in the switch to asyncio.


_local = threading.local()


def Context(children=None, **kwargs):  # noqa: N802
    """Like the React Conext API."""
    context = getattr(_local, "context", ChainMap())
    try:
        _local.context = context.new_child(kwargs)
        yield children
    finally:
        _local.context = context


def use_context(key, default=None):
    """Similar to the React use context API."""
    context: Mapping = getattr(_local, "context", ChainMap())
    return context.get(key, default)
