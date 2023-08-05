#!/usr/bin/env python3

import contextlib
import typing as t

from flask_gordon.ext import ArgParseExt
from torxtools.ctxtools import suppress_traceback

from . import app, rootpath

# Description for `./gl-webhooks --help`
description: str = r"""GL Webhooks is a project that provides GitLab functionalities via webhook endpoints."""

# Options for backends
options: t.Dict[str, t.Any] = {
    "static": {"redirect_to": "/api/ui/", "redirect_code": 308},
}


def main(middleware: str = "gunicorn") -> None:
    ctx = {"gunicorn": suppress_traceback, "flask": contextlib.nullcontext}[middleware]
    with ctx():
        # pylint: disable=global-statement,invalid-name
        global app
        app = ArgParseExt().init_app(app, middleware, cfgfilename="gl-webhooks.yml")
        app = app.configure(rootpath, middleware, options)
        app.run()


if __name__ == "__main__":
    main()
