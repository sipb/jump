import os

def require_env(var):
    val = os.getenv(var)
    if val is None:
        raise Exception("ENV variable `%s` is required." % var)
    return val
