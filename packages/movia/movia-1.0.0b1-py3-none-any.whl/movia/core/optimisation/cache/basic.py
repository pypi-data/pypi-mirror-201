#!/usr/bin/env python3

"""
** The not sofisticated cache decorators. **
--------------------------------------------
"""

import functools
import typing


def _get_hash_global(func_name: str, signature: typing.Hashable) -> object:
    """
    ** Try to get the content. **

    raises
    ------
    KeyError
        Il the element is not present.
    """
    ref = f"_{func_name}_cache_memory"
    return globals()[ref][signature]

def _set_hash_global(func_name: str, signature: typing.Hashable, res: object) -> None:
    """
    ** Saves the new result in the global dict. **
    """
    ref = f"_{func_name}_cache_memory"
    if ref not in globals():
        globals()[ref] = {}
    globals()[ref][signature] = res


def hash_cache(func) -> typing.Callable:
    """
    ** Shortcut func with hashable args. **
    """
    @functools.wraps(func)
    def func_shortcut(*args, **kwargs):
        signature = (args, ((k, kwargs[k]) for k in sorted(kwargs)))
        try:
            return _get_hash_global(func.__name__, signature)
        except KeyError:
            pass
        res = func(*args, **kwargs)
        _set_hash_global(func.__name__, signature, res)
        return res
    return func_shortcut
