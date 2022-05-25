def install(package_name):
    import pip
    try:
        pip.main(["install", "--user", "--user", "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org",
                  "--trusted-host", "files.pythonhosted.org", package_name])
    except Exception:
        return 0
    return 1


def parse(free, used, total):
    if free is not None or used is not None or total is not None:
        # throw Exception
        0
    else:
        0
