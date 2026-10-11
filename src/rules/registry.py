"""Immutable state registry. Missing jurisdictions fail explicitly, never default exempt."""

from collections.abc import Iterable
from types import MappingProxyType

from ..models import StateRequirement, normalize_state


class UnsupportedJurisdictionError(ValueError):
    """No reviewed rule module is available for this jurisdiction."""


class RulesRegistry:
    def __init__(self, requirements: Iterable[StateRequirement]) -> None:
        indexed: dict[str, StateRequirement] = {}
        for requirement in requirements:
            if requirement.state in indexed:
                raise ValueError(f"Duplicate state rules: {requirement.state}")
            indexed[requirement.state] = requirement
        self._requirements = MappingProxyType(indexed)

    @property
    def states(self) -> tuple[str, ...]:
        return tuple(sorted(self._requirements))

    def get(self, state: str) -> StateRequirement:
        code = normalize_state(state)
        try:
            return self._requirements[code]
        except KeyError as exc:
            raise UnsupportedJurisdictionError(f"No rules registered for {code}") from exc


from .states import (  # noqa: E402
    alabama,
    alaska,
    arizona,
    arkansas,
    california,
    colorado,
    connecticut,
    delaware,
    florida,
    georgia,
    hawaii,
    idaho,
    illinois,
    indiana,
    iowa,
    kansas,
    kentucky,
    louisiana,
    maine,
    massachusetts,
    michigan,
    minnesota,
    mississippi,
    missouri,
    montana,
    new_york,
    north_carolina,
    texas,
    washington,
    wyoming,
)

DEFAULT_REGISTRY = RulesRegistry(
    module.REQUIREMENT
    for module in (
        alabama,
        alaska,
        arizona,
        arkansas,
        california,
        colorado,
        connecticut,
        delaware,
        florida,
        georgia,
        hawaii,
        idaho,
        illinois,
        indiana,
        iowa,
        kansas,
        kentucky,
        louisiana,
        maine,
        massachusetts,
        michigan,
        minnesota,
        mississippi,
        missouri,
        montana,
        new_york,
        north_carolina,
        texas,
        washington,
        wyoming,
    )
)
