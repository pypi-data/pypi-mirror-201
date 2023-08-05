import gitlab as GitLab


def gitlab(app):
    cfg = app.settings["gitlab"]
    gl = GitLab.Gitlab(cfg["url"], private_token=cfg["token"])
    return gl
