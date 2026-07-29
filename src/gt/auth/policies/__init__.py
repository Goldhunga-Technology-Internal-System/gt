from ._user_policies import UserPolicies

__all__ = ["UserPolicies"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")
