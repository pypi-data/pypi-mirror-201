import importlib.util


def package_available(pkg_name):
    spec = importlib.util.find_spec(pkg_name)
    if spec is None:
        return False
    return True