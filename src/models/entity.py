"""Validated entity identities; registry status must be supplied explicitly."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class EntityType(StrEnum):
    LLC = "LLC"
    C_CORP = "C-Corp"
    LP = "LP"


class EntityStatus(StrEnum):
    GOOD_STANDING = "Good Standing"
    FORFEITED = "Forfeited"
    REVOKED = "Revoked"


_STATE_NAMES = (
    "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|"
    "District of Columbia|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|"
    "Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|"
    "Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|"
    "North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|"
    "South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|"
    "West Virginia|Wisconsin|Wyoming"
).split("|")
_STATE_CODES = (
    "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS "
    "MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY"
).split()
STATE_NAMES = dict(zip(_STATE_CODES, _STATE_NAMES, strict=True))


def normalize_state(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("State must be a US state name or postal abbreviation")
    cleaned = value.strip()
    if cleaned.upper() in STATE_NAMES:
        return cleaned.upper()
    for code, name in STATE_NAMES.items():
        if cleaned.casefold() == name.casefold():
            return code
    raise ValueError(f"Unsupported US jurisdiction: {value!r}")


@dataclass(frozen=True, slots=True)
class Entity:
    legal_name: str
    entity_type: EntityType
    domestic_state: str
    formation_date: date
    sos_entity_id: str | None
    status: EntityStatus

    def __post_init__(self) -> None:
        if not isinstance(self.legal_name, str) or not self.legal_name.strip():
            raise ValueError("legal_name must be nonempty")
        object.__setattr__(self, "legal_name", self.legal_name.strip())
        object.__setattr__(self, "entity_type", EntityType(self.entity_type))
        object.__setattr__(self, "status", EntityStatus(self.status))
        object.__setattr__(self, "domestic_state", normalize_state(self.domestic_state))
        if type(self.formation_date) is not date:
            raise ValueError("formation_date must be a date (without a time component)")
        if self.sos_entity_id is not None:
            if not isinstance(self.sos_entity_id, str) or not self.sos_entity_id.strip():
                raise ValueError("sos_entity_id must be a nonempty string or None")
            object.__setattr__(self, "sos_entity_id", self.sos_entity_id.strip())
