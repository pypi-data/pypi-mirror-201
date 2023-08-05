import os
import typing as t

from flasket import Flasket

__all__: t.List[str] = [
    "rootpath",
    "app",
]

rootpath: str = os.path.dirname(__file__)

# pylint: disable=invalid-name
app = Flasket(__name__)
