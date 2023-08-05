""" /models/badges/

Generate, cache and return badges from shields.io

files:
  gl_webhooks/models/badges.py
  tests/models/test_badges.py

"""

import os
from copy import deepcopy
from hashlib import sha1
from mimetypes import guess_type

import requests
from boltons.fileutils import atomic_save

CACHEDIR_SUFFIX = "badges"

# FIXME:
RD_WEBHOOKS_CACHEDIR = "/tmp/badges"


def build_query_string(params):
    if not params:
        return ""
    if isinstance(params, str):
        return params
    return "&".join(f"{k}={v}" for k, v in sorted(params.items()))


class StaticBadge:
    """Return a static badge from shields.io

    Badge is, by default, a svg.
    """

    # These are the only params used for the cache hashkey:
    HASHKEY_PARAMS = {"message", "label", "color", "style", "logo", "logoColor", "logoWidth", "labelColor"}
    DEFAULT_URL = "https://img.shields.io/static/v1.{extension}?{query}"

    def __init__(self, **kwargs):
        """Initialize a badge with unknown content and a default type of svg.

        We filter out values that we do not use for the cache key or that we
        do not pass to shields.io (such as cacheSeconds)
        """
        self._content_type = None
        self._data = None
        self._fileext = "svg"
        self._url = StaticBadge.DEFAULT_URL

        # Filter values to have a fixed set of keys present
        self._params = {k: kwargs.get(k) for k in StaticBadge.HASHKEY_PARAMS if kwargs.get(k, None) is not None}
        # trim the values since shields does it also
        for k, v in self._params.items():
            if isinstance(v, str):
                self._params[k] = v.strip()
        self.get()

    @property
    def content_type(self):
        """Return content_type, fetching ressource if necessary"""
        return self._content_type

    @property
    def data(self):
        """Return data_type, fetching ressource if necessary"""
        return self._data

    @property
    def fileext(self):
        """Return file type as a file extension"""
        return self._fileext

    @property
    def params(self):
        """Return params used for query"""
        return self._params

    @property
    def url(self):
        """Return URL string to fetch to fill ressource"""
        return self._url.format(extension=self.fileext, query=self.query)

    @property
    def query(self):
        """Return query string to fetch to fill ressource"""
        # shields.io is permissive in different ways depending on which endpoint we call.
        # for example:
        #   - https://img.shields.io/badge/label--color
        #     => considers message=""
        #   - https://img.shields.io/static/v1.svg?label=label&message=&color=color
        #     => considers this to be an error
        #
        params = deepcopy(self.params)
        # fixup the 'message' in params:
        # - we know message will be trimmed,
        # - we know that empty string is an error
        if params["message"] == "":
            params["message"] = " "
        return build_query_string(params)

    def get(self):
        """Fetchs the ressource by downloading it from shields.io."""
        rv = requests.get(self.url, timeout=10)
        # TODO: Handle rv.status_code errors
        self._content_type = rv.headers["Content-Type"]
        self._data = rv.content

    @classmethod
    def str_to_args(cls, badge):
        if badge.endswith(".svg"):
            badge = badge[:-4]

        # Double underscores map to spaces
        badge.replace("__", "%5F")
        badge.replace("_", "%20")
        badge.replace(" ", "%20")

        # shields.io binds dashdash (--) to message, not label:
        #   label---message---color => message = "-message-"
        # For that reason, start from the back
        parts = badge.split("-")
        color = parts.pop()

        # hackety hack: replace dash with underscore to mark a double dash
        text = "-".join(parts)
        text = text.replace("---", "-_")
        text = text.replace("--", "_")
        parts = text.split("-")

        # too many parts corresponds to a 404 error
        if len(parts) >= 3:
            return False

        label = ""
        if len(parts) > 1:
            label = parts.pop(0).replace("--", "%2D").replace("_", "%2D")
        message = "-".join(parts).replace("--", "%2D").replace("_", "%2D")

        return {"label": label.strip(), "message": message.strip(), "color": color.strip()}


class CachedBadge(StaticBadge):
    """Return a static badge from shields.io unless it was already save in cache"""

    def __init__(self, **kwargs):
        self._filepath = None
        self._fileuuid = None

        path = os.path.join(RD_WEBHOOKS_CACHEDIR, CACHEDIR_SUFFIX)
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        self._cachedir = path
        StaticBadge.__init__(self, **kwargs)

    @property
    def cachedir(self):
        return self._cachedir

    @property
    def fileuuid(self):
        if self._fileuuid is not None:
            return self._fileuuid
        k = sha1(self.query.encode("utf-8")).hexdigest()  # nosec
        k = k[:4] + "/" + k[4:]
        k = k[:2] + "/" + k[2:]
        self._fileuuid = k
        return self._fileuuid

    @property
    def filepath(self):
        if self._filepath is not None:
            return self._filepath
        path = os.path.join(self.cachedir, self.fileuuid + "." + self.fileext)
        self._filepath = path
        return self._filepath

    def load(self):
        path = self.filepath
        if not os.path.isfile(path):
            return False

        self._content_type = guess_type(path)[0]
        with open(path, "rb") as fd:
            self._data = fd.read()
        return True

    def save(self):
        folder = os.path.dirname(self.filepath)
        os.makedirs(folder, exist_ok=True)
        with atomic_save(self.filepath, overwrite=False) as fd:
            fd.write(self._data)

    def get(self):
        if self.load():
            return
        StaticBadge.get(self)
        self.save()

    @classmethod
    def as_response(cls, app, **kwargs):
        badge = CachedBadge(**kwargs)
        response = app.make_response(badge.data)
        response.headers["Content-Type"] = badge.content_type
        return response
