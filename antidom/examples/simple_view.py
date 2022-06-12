"""Test the view protocol and decorator."""

from antidom import VDOM
from antidom.view import get_view
from . import Store


def main() -> VDOM:
    this_view = get_view()
    result = this_view.__vdom__()
    return result
