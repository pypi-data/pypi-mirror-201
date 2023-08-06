from .dequeai import init, finish, log, log_artifact, register_artifacts

__all__ = ['init', 'finish', 'log', 'log_artifact', 'register_artifacts']

globals().update({name:obj for name,obj in locals().items() if callable(obj) })