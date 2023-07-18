from collections.abc import MutableSet

from ..types import ConfiguredVerifier, CostDict


class Portfolio(MutableSet):
    """_summary_."""

    def __init__(self, *cvs: ConfiguredVerifier):
        self._pf_set: set[ConfiguredVerifier] = set(cvs)
        self._costs: CostDict = {}

    def __contains__(self, cv: ConfiguredVerifier):
        return cv in self._pf_set

    def __iter__(self):
        return iter(self._pf_set)

    def __len__(self):
        return len(self._pf_set)

    def __str__(self):
        res = ""

        for cv in self:
            res += str(cv) + "\n"

        return res

    def add(self, cv: ConfiguredVerifier):
        self._pf_set.add(cv)

    def discard(self, cv: ConfiguredVerifier):
        self._pf_set.discard(cv)

    def update_costs(self, costs: CostDict):
        pass
