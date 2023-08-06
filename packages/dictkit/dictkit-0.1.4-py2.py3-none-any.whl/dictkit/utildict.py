from __future__ import annotations
from collections import ChainMap
from typing import overload, Iterable, Mapping, TypeVar, Literal
from copy import copy


def is_valid_normal_iterable(item) -> bool:
    """
    Returns True if the average human would say, "Yes, that looks like a
    regular iterable to me"
    """
    if not isinstance(item, Iterable):
        return False
    if isinstance(item, Mapping):
        return False
    if isinstance(item, (str, bytes, bytearray)):
        return False
    return True


# Key-value types of current object
K = TypeVar("K")
V = TypeVar("V")
# Key-value types of external arguments passed in
K2 = TypeVar("K2")
V2 = TypeVar("V2")


class UtilDict(dict[K, V]):
    """
    A better dictionary. Allows getting, setting, adding, and dropping items in useful ways,
    supporting dot notation item access, and getting/setting multiple keys and values at once.

    Renders in nested-json style structure, while maintaining default Python value formatting.

    Get items with dot notation, if you wish

    Get multiple items at a time: `my_dict[['a', 'b']]` -> {'a': x, 'b': y}
      - Returns new, filtered instance

    Set multiple items at a time: `my_dict[['a', 'b']] = 10, 11`

    Set same value to multiple items: `my_dict[['a', 'b']] = 10`

    Add items, while returning a modified copy of self
      - `my_dict.add(a=5)` -> {<existing key/values>, 'a': 5}

    Drop items, while returning a modified copy of self
      - `my_dict.drop('a', 'b')` -> {<key/values excluding 'a' and 'b'>}

    Accepts a variety of argument types at creation
      - Accepts other dictionaries, iterables (lists or tuples) of
        length 2, to make key-value pairs from.
      - 2-element iterables will be converted to dictionaries with one key/value pair
        before being combined with other arguments

    Examples
    --------

    GPT-4 came up with and wrote all of these, given nothing other than the source code

    It works just like a normal dictionary at first.
    >>> sd = UtilDict(a=1,b=2,c=3)
    >>> sd
    {
       'a': 1,
       'b': 2,
       'c': 3
    }

    But can initialize with a variety of types
    >>> sd = UtilDict({"a": 1}, [("b", 2)], c=3)
    >>> sd
    {
       'a': 1,
       'b': 2,
       'c': 3
    }

    Dot notation access
    >>> sd = UtilDict(a=1, b=2, c=3)
    >>> sd.a
    1

    Get multiple items at once
    >>> sd = UtilDict(a=1, b=2, c=3)
    >>> selected_items = sd[["a", "c"]]
    >>> selected_items
    {
       'a': 1,
       'c': 3
    }

    Set multiple items at once
    >>> sd = UtilDict(a=1, b=2, c=3)
    >>> sd[["a", "c"]] = 10, 30
    >>> sd
    {
       'a': 10,
       'b': 2,
       'c': 30
    }

    Set the same value to multiple keys at once
    >>> sd = UtilDict(a=1, b=2, c=3)
    >>> sd[["a", "c"]] = 99
    >>> sd
    {
       'a': 99,
       'b': 2,
       'c': 99
    }

    Add items from a variety of types
    >>> sd = UtilDict(a=1, b=2)
    >>> sd2 = sd.add({"c": 3}, ("d", 4), e=5)
    >>> sd2
    {
       'a': 1,
       'b': 2,
       'c': 3,
       'd': 4,
       'e': 5
    }

    Drop multiple items at once
    >>> sd = UtilDict(a=1, b=2, c=3, d=4)
    >>> sd2 = sd.drop("a", "c")
    >>> sd2
    {
       'b': 2,
       'd': 4
    }
    """

    def __init__(self, *args, **kwargs):
        if args:
            if len(args) == 2:
                # Special case. If two normal iterables, zip em together
                if is_valid_normal_iterable(args[0]) and is_valid_normal_iterable(
                    args[1]
                ):
                    return super().__init__(zip(*args), **kwargs)  # type:ignore

            args = [self._iterable_to_dict(arg) for arg in args]
            args = (ChainMap(*list(reversed(args))),)
        super().__init__(*args, **kwargs)

    def add(
        self, *args: Mapping[K2, V2] | Iterable, **kwargs: V2
    ) -> UtilDict[K | K2, V | V2]:
        """
        Add items, returning a copy with the new items.

        Parameters
        ----------
        *args
            Dictionaries or 2-element iterables
            to make key-value pairs from.
        **kwargs
            Key-value pairs to update.

        Returns
        -------
        Self
            A new UtilDict instance containing the original items and the added items.

        Examples
        --------
        >>> sd = UtilDict(a=1, b=2)
        >>> sd.add(c=3)
        {
           'a': 1,
           'b': 2,
           'c': 3
        }
        >>> sd.add({"d": 4}, e=5)
        {
           'a': 1,
           'b': 2,
           'd': 4,
           'e': 5
        }
        """
        new = self.copy()

        args = [self._iterable_to_dict(arg) for arg in args]  # type:ignore
        for mapping in args:
            new.update(mapping)

        new.update(kwargs)
        return new

    @overload
    def drop(self, *keys, inplace: bool) -> None:
        ...

    @overload
    def drop(self, *keys) -> UtilDict:
        ...

    def drop(self, *keys, inplace=False):
        """
        Remove items by key, returning a copy with the items dropped.

        Parameters
        ----------
        *keys
            Keys of the items to remove.
        inplace : bool, optional, default: False
            If True, the items are removed from the UtilDict inplace, modifying the original instance.

        Returns
        -------
        Self or None
            A new updated instance, or None if inplace=True.

        Examples
        --------
        >>> sd = UtilDict(a=1, b=2, c=3)
        >>> sd.drop("a")
        {
           'b': 2,
           'c': 3
        }
        >>> sd.drop("b", "c", inplace=True)
        >>> sd
        {
           'a': 1
        }
        """
        new = self if inplace else self.copy()

        if len(keys) == 1:
            if isinstance(keys[0], list):
                keys = keys[0]

        for k in keys:
            new.pop(k)

        if not inplace:
            return new

    @overload
    def deep_uniform(self, reverse: Literal[False]) -> UtilDict[K, V]:
        ...

    @overload
    def deep_uniform(self, reverse: Literal[True]) -> dict:
        ...

    def deep_uniform(self, reverse=False):
        """
        Recursively convert all child instances of `dict` to
        Self's type.

        If `reverse=True`, then the opposite happens. Converts all nested UtilDict
        to `dict`, and returns a `dict`
        """

        def uniform(value):
            if isinstance(value, (UtilDict, dict)):
                value = {k: uniform(v) for k, v in value.items()}
                if not reverse:
                    value = UtilDict(value)
            elif isinstance(value, (list, tuple)):
                value = type(value)(uniform(x) for x in value)
            return value

        new = self.copy()
        for key, value in new.items():
            new[key] = uniform(value)

        if reverse:
            return dict(**new)
        return new

    def __getattr__(self, k):
        return self.__getitem__(k)

    def __setitem__(self, key, val):
        special_key_types = (list, type(...))
        if not isinstance(key, special_key_types):
            return super().__setitem__(key, val)

        if isinstance(key, type(...)):
            if isinstance(val, dict):
                for k, v in val.items():
                    super().__setitem__(k, v)
                return
            raise ValueError(val)

        assert isinstance(key, list), type(key)

        if isinstance(val, tuple):
            if len(val) == len(key):
                for k, v in zip(key, val):
                    super().__setitem__(k, v)
            else:
                raise ValueError(
                    "Number of values assigned must equal number of keys assigning to"
                )
            return

        for k in key:
            super().__setitem__(k, copy(val))

    @overload
    def __getitem__(self, key: K) -> V:
        ...

    @overload
    def __getitem__(self, key: list[K]) -> UtilDict[K, V]:
        ...

    def __getitem__(self, key):
        if not isinstance(key, list):
            return super().__getitem__(key)

        new = type(self).__new__(type(self))
        new.update(
            {k: super(type(self), self).__getitem__(k) for k in key}
        )  # Note: `super()` won't work inside comprehensions, so we have to pass type and instance directly
        return new

    def copy(self) -> UtilDict:
        new = type(self).__new__(self.__class__)
        new.update({k: copy(v) for k, v in self.items()})
        return new

    def __copy__(self) -> UtilDict:
        return self.copy()

    def _iterable_to_dict(self, arg) -> dict:

        if isinstance(arg, Mapping):
            return dict(arg)

        if not isinstance(arg, Iterable):
            # Let dict throw the error if not hashable
            return {arg: self.get(arg)}

        try:
            return dict(arg)
        except Exception:
            pass

        if is_valid_normal_iterable(arg) and hasattr(arg, "__len__"):
            elems = list(arg)
            if len(elems) == 2:
                if all(is_valid_normal_iterable(a) for a in elems):
                    return dict(zip(*elems))
                return {elems[0]: elems[1]}

        try:
            # When it's an iterable with valid keys but no values,
            # Set each key to None, but don't override where self already contains
            # a value for the key
            return {x: self.get(x) for x in arg}
        except Exception:
            pass

        # Ah, so we've got values that aren't valid keys. Use them as values instead lmao
        return {i: self.get(v) for i, v in enumerate(arg)}

    def render(self, **kwargs) -> str:
        from dictkit.render import render

        return render(self, **kwargs)

    def json(self, indent: int = 2, **kwargs) -> str:
        import json

        def fmt(dic) -> dict:
            return {
                k: v
                if isinstance(v, (int, float, str, list, tuple))
                else fmt(v)
                if isinstance(v, dict)
                else str(v)
                for k, v in dic.items()
            }

        dic = fmt(self)
        return json.dumps(dic, indent=indent, **kwargs)

    def __repr__(self):
        return self.render()


if __name__ == "__main__":
    from doctest import testmod

    testmod()
