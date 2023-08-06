import gitlab as GitLab


def gitlab(settings):
    cfg = settings["gitlab"]
    gl = GitLab.Gitlab(cfg["url"], private_token=cfg["token"])
    return gl
