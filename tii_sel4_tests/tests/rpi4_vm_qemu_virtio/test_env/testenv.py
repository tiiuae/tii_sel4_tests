import os

def init(*args, **kwargs) -> None:
    os.environ["LG_ENV"] = os.path.join(os.path.realpath(os.path.dirname(__file__)), "env.yaml")
