""" /api/badges/* endpoint

files:
  gl_webhooks/api/badges/static.py
  gl_webhooks/api/badges/static.yml
  tests/api/badges/test_static.py

TODO:
  - We could add raster image support (png)
  - Add identical params from static.svg to the badges 'get' method (for logo, ... support)
"""


from flasket import endpoint

from gl_webhooks.models.badges import CachedBadge, StaticBadge

BADGE_404_NOT_FOUND = {"label": "404", "message": "badge not found", "color": "red"}


@endpoint
def get(*, app, badge, **_kwargs):
    """/api/badges/{template}

    Return a badge from cache if we already have it, or from shields.io otherwise.

    All static badges are cached by default on disk.
    """
    args = StaticBadge.str_to_args(badge)
    if not args:
        rv = CachedBadge.as_response(app, **BADGE_404_NOT_FOUND)
        return rv, 404
    return CachedBadge.as_response(app, **args)


@endpoint
def svg(*, app, **kwargs):
    """/api/badges/static.svg

    Return a badge from cache if we already have it, or from shields.io otherwise.
    """
    return CachedBadge.as_response(app, **kwargs)
