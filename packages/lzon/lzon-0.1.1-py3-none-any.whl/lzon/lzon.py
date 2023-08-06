import json

from functools import cache
from contextlib import suppress
from typing import Union, Any



JSONValue = Union[None, bool, int, str, 'JSONObject']
JSONObject = list[JSONValue] | dict[str, JSONValue]


class LazyJSON:
    """
    A wrapper for a JSON object
    that only loads entries on request

    OBS! This is meant as read-only.
    """

    data: JSONObject


    def __init__(self, data: JSONObject) -> None:
        self.data = data

    def __str__(self) -> str:
        return str(self.data)

    @cache
    def __getitem__(self, key: Union[int, str]) -> JSONValue:
        return loads(self.data[key])


    def get(self, key: Union[int, str], default: Any = None) -> JSONValue:
        """
        Return the value for key if key is in the dictionary, else default.
        """
        
        if isinstance(key, int):
            with suppress(IndexError):
                return self[key]

        if isinstance(key, str):
            with suppress(KeyError):
                return self[key]

        return default


def loads(data: JSONValue) -> LazyJSON | JSONValue:
    """
    Parse data into a lazy loading JSON object.

    The value will be returned as is,
    if it is not a list or dictionary,
    or a string that can be interpreted as JSON.
    """

    # Lists and dictionaries can be used for `LazyJSON`
    if isinstance(data, (list, dict)):
        return LazyJSON(data)

    # Attempt to load strings as JSON
    if isinstance(data, str):
        try:
            data = loads(json.loads(data))
            return data
        except json.JSONDecodeError:
            return data

    # Return all other data types as is
    return data