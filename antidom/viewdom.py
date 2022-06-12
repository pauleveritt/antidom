"""ViewDOM."""
from __future__ import annotations

import functools
import re
from collections.abc import ByteString
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable, Any, Mapping, Sequence, cast
from typing import Generator, Literal
from typing import Optional

from antidote import world

from .tagged import tag, ParseError


@dataclass(frozen=True)
class VDOMNode:
    """Implementation of a node with three slots."""

    __slots__ = ["tag", "props", "children"]
    tag: str
    props: Mapping[str, object]
    children: list[str | VDOMNode]


VDOM = Sequence[VDOMNode] | VDOMNode

RE_COLLAPSE = re.compile(r"^[^\S\n]*\n\s*|[^\S\n]*\n\s*$")


def collapse_ws(string: str) -> Any:
    return RE_COLLAPSE.sub("", string)


def get_simple_token(scanner: Scanner, regex: re.Pattern[str]) -> str:
    match = scanner.match(regex)
    if not match:
        raise ParseError("no token found")
    token: str = match.group(0)
    if token[0] in "\"'" and token[0] == token[-1]:
        token = token[1:-1]
    return token


class Scanner:
    def __init__(self, strings: tuple[str, ...]):
        self._strings = strings
        self._index = 0
        self._start = 0

    def peek(self) -> tuple[bool, str | int | None]:
        if self._index < len(self._strings):
            if self._start < len(self._strings[self._index]):
                return True, self._strings[self._index][self._start]
            if self._index < len(self._strings) - 1:
                return False, self._index
        return False, None

    def pop(self) -> tuple[bool, int | object]:
        is_text, value = self.peek()
        if is_text:
            self._start += 1
        elif value is not None:
            self._index += 1
            self._start = 0
        return is_text, value

    def match(self, regex: re.Pattern[str]) -> re.Match[str] | None:
        if self._index < len(self._strings):
            match = regex.match(self._strings[self._index], self._start)
            if match:
                self._start = match.end()
                return match
        return None

    def search(self, regex: Any) -> Any:
        start = self._start
        prefix: list[tuple[bool, int | str]] = []
        for index in range(self._index, len(self._strings)):
            match = regex.search(self._strings[index], start)
            if match:
                if start < match.start():
                    prefix.append((True, self._strings[index][start:match.start()]))
                self._index = index
                self._start = match.end()
                return match, tuple(prefix)
            if start < len(self._strings[index]):
                prefix.append((True, self._strings[index][start:]))
            if index < len(self._strings) - 1:
                prefix.append((False, index))
            start = 0
        return None, ()

    def flush(self) -> Any:
        flushed: list[tuple[bool, str | int]] = []
        start = self._start
        for index in range(self._index, len(self._strings)):
            if start < len(self._strings[index]):
                flushed.append((True, self._strings[index][start:]))
            if index < len(self._strings) - 1:
                flushed.append((False, index))
            start = 0
        self._index = len(self._strings)
        self._start = 0
        return tuple(flushed)


TAG_OR_COMMENT_START = re.compile(r"<(?:!--|/)?")
COMMENT_END = re.compile(r"-->")
TAG_NAME = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/\s]+")
PROP_NAME = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/=\s]+")
WHITESPACE = re.compile(r"\s*")
SPREAD = re.compile(r"../examples/components/simple_htm")
TAG_END = re.compile(r"/?>")
DOUBLE_QUOTE = re.compile(r"\"")
SINGLE_QUOTE = re.compile(r"'")
PROP_VALUE_END = re.compile(r"(?=/>|>|\s)")


def htm_parse(strings: tuple[str, ...]) -> list[Any]:
    scanner = Scanner(strings)

    ops: list[Any] = []
    while True:
        match, prefix = scanner.search(TAG_OR_COMMENT_START)
        for is_text, value in (prefix if match else scanner.flush()):
            if is_text:
                value = collapse_ws(value)
                if value:
                    ops.append(("CHILD", False, collapse_ws(value)))
            else:
                ops.append(("CHILD", True, value))
        if not match:
            break

        if match.group(0) == "<!--":
            match, _ = scanner.search(COMMENT_END)
            if not match:
                raise ParseError("missing comment end")
            continue

        elif match.group(0) == "</":
            slash = True
        else:
            slash = False
            is_text, value = scanner.peek()
            if is_text:
                this_tag = get_simple_token(scanner, TAG_NAME)
                ops.append(("OPEN", False, this_tag))
            elif value is not None:
                scanner.pop()
                ops.append(("OPEN", True, value))
            else:
                raise ParseError("unexpected end of data")

        while True:
            scanner.match(WHITESPACE)
            is_text, value = scanner.peek()
            if not is_text:
                if value is None:
                    raise ParseError("unexpected end of data")
                raise ParseError("expression not allowed")

            match = scanner.match(TAG_END)
            if match:
                if match.group(0) == "/>":
                    slash = True
                if slash:
                    ops.append(("CLOSE",))
                break

            match = scanner.match(SPREAD)
            in_text, value = scanner.peek()
            if match and not in_text and value is not None:
                _, index = scanner.pop()
                if not slash:
                    ops.append(("SPREAD", True, index))
                continue

            prop = get_simple_token(scanner, PROP_NAME)
            is_text, value = scanner.peek()
            if not is_text:
                if value is None:
                    raise ParseError("unexpected end of data")
                raise ParseError("expression not allowed here")

            if value.isspace() or value in ("/", ">"):
                if not slash:
                    ops.append(("PROP_SINGLE", prop, False, True))
            elif value == "=":
                scanner.pop()

                is_text, value = scanner.peek()
                if is_text and value == "\"":
                    scanner.pop()
                    match, prefix = scanner.search(DOUBLE_QUOTE)
                elif is_text and value == "'":
                    scanner.pop()
                    match, prefix = scanner.search(SINGLE_QUOTE)
                else:
                    match, prefix = scanner.search(PROP_VALUE_END)

                if not match:
                    raise ParseError("unexpected end of data")

                if not prefix:
                    ops.append(("PROP_SINGLE", prop, False, ""))
                elif len(prefix) == 1:
                    is_text, value = prefix[0]
                    ops.append(("PROP_SINGLE", prop, not is_text, value))
                else:
                    ops.append(("PROP_MULTI", prop, prefix))
            else:
                raise ParseError("invalid character")

    count = 0
    for op in ops:
        if op[0] == "OPEN":
            count += 1
        elif op[0] == "CLOSE":
            count -= 1
        if count < 0:
            raise ParseError("closing unopened tags")
    if count > 0:
        raise ParseError("all opened tags not closed")
    return ops


HtmEvalValue = str | VDOMNode
HtmEval = HtmEvalValue | Sequence[HtmEvalValue]


def htm_eval(
        h: Callable[..., object],
        ops: list[Any],
        values: tuple[type],
) -> HtmEval:
    root: list[HtmEvalValue] = []
    stack: list[tuple[Any, Any, Any]] = [("", {}, root)]

    for op in ops:
        if op[0] == "OPEN":
            _, value, this_tag = op
            stack.append((values[this_tag] if value else this_tag, {}, []))
        elif op[0] == "CLOSE":
            this_tag, props, children = stack.pop()
            stack[-1][2].append(h(this_tag, props, children))
        elif op[0] == "SPREAD":
            _, value, item = op
            this_tag, props, children = stack[-1]
            props.update(values[item] if value else item)
        elif op[0] == "PROP_SINGLE":
            _, attr, value, item = op
            this_tag, props, children = stack[-1]
            props[attr] = values[item] if value else item
        elif op[0] == "PROP_MULTI":
            _, attr, items = op
            this_tag, props, children = stack[-1]
            props[attr] = "".join(value if is_text else str(values[value]) for (is_text, value) in items)
        elif op[0] == "CHILD":
            _, value, item = op
            this_tag, props, children = stack[-1]
            children.append(values[item] if value else item)
        else:
            raise ValueError("unknown op")

    if len(root) == 1:
        return root[0]
    return root


def htm(cache_maxsize: int = 128) -> Callable[[str], VDOM]:
    """The callable function to act as decorator."""
    cached_parse = functools.lru_cache(maxsize=cache_maxsize)(htm_parse)

    @tag
    def __htm(strings: tuple[str, ...], values: tuple[type]) -> HtmEval:
        ops = cached_parse(strings)
        return htm_eval(VDOMNode, ops, values)

    return cast(Callable[[str], VDOM], __htm)


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
    elif hasattr(value, '__vdom__'):
        # E.g. a dataclass with an __vdom__ method
        vdom = value.__vdom__()
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
    full_props = props | dict(children=children)  # noqa

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
