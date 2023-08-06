import os
import typing as t

from flask_gordon.ext import CeleryExt
from flasket import Flasket

__all__: t.List[str] = [
    "app",
    "rootpath",
]

rootpath: str = os.path.dirname(__file__)

# pylint: disable=invalid-name
app = Flasket(__name__)
celery = CeleryExt().init_app(app)
CeleryExt.load(__name__, __file__)
