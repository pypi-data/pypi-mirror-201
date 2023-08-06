from __future__ import annotations
import re
from typing import Any, Literal

QuoteOption = bool | Literal["keys"] | Literal["values"]

def render(
    obj, indent: int = 3, quote: QuoteOption = True, line_spacing=1, shift=" "
) -> FormattedReprStr:
    """
    Represent nested dicts, lists, tuples, with json structure, but Python format.
    Displayed content appears as it would when printed, but with nested indentations.

    - Values with newline characters (such as DataFrames, or formatted text) will be placed
      on a new line and indented uniformly.
    - Can display any object, unlike `json.dumps()` which requires arguments to be json serializable.
    ---
    To my knowledge, no tool yet exists from popular libraries.

    Examples
    --------

    >>> lst = [int,"two",{"three":3,"four":"4"},("five","six")]
    >>> s = render(lst)
    >>> s
    [
       <class 'int'>,
       'two',
       {
          'three': 3,
          'four': '4'
       },
       (
          'five',
          'six'
       )
    ]

    Values multi-line formatting are reformatted to maintain their
    original appearance. List elements will indent uniformly.
    Dict values (if multi-line) will start on its own line, below its key,
    with extra indentation.
    >>> fmt_str = '''|------|
    ... |      |
    ... |------|'''
    >>> print(fmt_str)
    |------|
    |      |
    |------|
    >>> lst = [
    ...     'list element',
    ...     fmt_str,
    ...     'list element',
    ...     {
    ...         'key': 'val',
    ...         'formatted string': fmt_str,
    ...         'key2': 'val2',
    ...     }
    ... ]

    # >>> render(lst, quote=False)  # can't get doctest to work for this
    # [
    #    list element,
    #    |------|
    #    |      |
    #    |------|,
    #    list element,
    #    {
    #       key: val,
    #       formatted string:
    #          |------|
    #          |      |
    #          |------|,
    #       key2: val2
    #    }
    # ]

    This is most practical for things like DataFrames
    >>> from pandas import DataFrame
    >>> df = DataFrame([[1, 2, 3], [4, 55, 6]],
    ...                columns=["ONE", "TWO", "THREE"])
    >>> df
       ONE  TWO  THREE
    0    1    2      3
    1    4   55      6

    DataFrame is moved to a separate line and indented beneath
    its key
    >>> dct = {"a":{"x":'y',"df":df},"list":['a','b']}

    # >>> render(dct) # Can't get doctest to work for this
    # {
    #    'a': {
    #       'x': 'y',
    #       'df':
    #             ONE  TWO  THREE
    #          0    1    2      3
    #          1    4   55      6
    #    },
    #    'list': [
    #       'a',
    #       'b'
    #    ]
    # }

    Notice quotes were placed around string keys and values.
    We can disable this behavior for keys, values, or both.
    >>> dct = {
    ...     1: "1",
    ...     "2": 2,
    ...     "3": "3",
    ... }
    >>> render(dct, quote='keys')  # keys or values only
    {
       1: 1,
       '2': 2,
       '3': 3
    }
    >>> render(dct, quote=False)  # no quotes
    {
       1: 1,
       2: 2,
       3: 3
    }

    Custom indentation
    >>> dct = {'a':{'b':{'c':0},'d':{'e':0}}}
    >>> render(dct, indent=1, quote=False)
    {
     a: {
      b: {
       c: 0
      },
      d: {
       e: 0
      }
     }
    }

    Spaced outputs
    >>> render(['a',df,'b','c'], line_spacing=2)
    [
    <BLANKLINE>
       'a',
    <BLANKLINE>
          ONE  TWO  THREE
       0    1    2      3
       1    4   55      6,
    <BLANKLINE>
       'b',
    <BLANKLINE>
       'c'
    <BLANKLINE>
    ]
    """
    if isinstance(quote, bool):
        quote_keys, quote_values = quote, quote
    else:
        quote_keys = True if quote == "keys" else False
        quote_values = True if quote == "values" else False

    def fmt_val(obj) -> str:
        return fmt(obj, quote_values) + ","

    def fmt_key(obj) -> str:
        if not obj:
            return ""
        return fmt(obj, quote_keys) + ": "

    def nextline(indent) -> str:
        return "\n" * line_spacing + shift * indent

    def indent_existing_in_dict(val: str, ind: int) -> str:
        if "\n" in val:
            if not val.startswith("\n"):
                val = "\n" + val
        new_indent = ind + indent
        return re.sub(r"\n([^\n])", r"\n" + shift * new_indent + r"\1", val)

    def indent_existing(val: str, ind: int) -> str:
        new_indent = ind
        return re.sub(r"\n([^\n])", r"\n" + shift * new_indent + r"\1", val)

    def _render(key: Any = "", val: Any = "", ind: int = 0, s: str = "", from_dict=False) -> str:
        open, close = get_enclosure(val)
        end = nextline(ind) + close + ","
        s += nextline(ind) + fmt_key(key) + open

        if not open:
            if from_dict:
                return s + indent_existing_in_dict(fmt_val(val), ind)
            return s + indent_existing(fmt_val(val), ind)

        items = val.items() if isinstance(val, dict) else [("", x) for x in val]

        from_dict = True if isinstance(val, dict) else False
        rendered_items = "".join(
            [_render(k, v, ind + indent, from_dict=from_dict) for k, v in items]
        ).removesuffix(",")

        return s + rendered_items + end

    from_dict = True if isinstance(obj, dict) else False
    return FormattedReprStr(_render("", obj, 0, "", from_dict=from_dict).lstrip("\n").removesuffix(","))


def get_enclosure(obj) -> tuple[str, str]:
    if isinstance(obj, list):
        return ("[", "]")
    if isinstance(obj, tuple):
        return ("(", ")")
    if isinstance(obj, dict):
        return ("{", "}")
    return ("", "")


def fmt(obj, quote=True) -> str:
    if isinstance(obj, str):
        if not obj or quote:
            return "'" + obj + "'"
    return str(obj)



class FormattedReprStr(str):
    r"""
    >>> s = "{\n   'a': 6,\n   'b': {\n      'c': 7\n   },\n   'd': 8\n}"
    >>> s
    "{\n   'a': 6,\n   'b': {\n      'c': 7\n   },\n   'd': 8\n}"
    >>> fs = FormattedReprStr(s)
    >>> fs
    {
       'a': 6,
       'b': {
          'c': 7
       },
       'd': 8
    }
    """
    def __repr__(self):
        return self


if __name__ == "__main__":
    import doctest
    doctest.testmod()

