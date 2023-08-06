from oak9.sac_framework.core.types import Context


class Capability():
    _Id: str = None
    _Name: str = None

    def __init__(self, context: Context):
        # apply business context
        self._context = context

    def id(self):
        return self._Id

    def name(self):
        return self._Name
