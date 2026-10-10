"""Cross-border screening with explainable decisions and separate remedy flags."""

import re
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

from .entity import Entity, EntityStatus, normalize_state
from .requirements import Activity, BusinessPresence, EntityRequirement, LegalSource

if TYPE_CHECKING:
    from ..rules.registry import RulesRegistry


class QualificationDecision(StrEnum):
    REQUIRED = "required"
    NOT_REQUIRED = "not_required"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True, slots=True)
class RegisteredAgent:
    name: str
    state: str
    street_address: str
    is_physical_address: bool = True

    def __post_init__(self) -> None:
        for attr in ("name", "street_address"):
            value = getattr(self, attr)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{attr} must be nonempty")
            object.__setattr__(self, attr, value.strip())
        object.__setattr__(self, "state", normalize_state(self.state))
        if type(self.is_physical_address) is not bool:
            raise ValueError("is_physical_address must be boolean")

    @property
    def is_po_box(self) -> bool:
        return bool(
            re.search(
                r"\b(?:p\.?\s*o\.?|post\s+office)\s*box\b", self.street_address, re.IGNORECASE
            )
        )


@dataclass(frozen=True, slots=True)
class AuditResult:
    entity: Entity
    target_state: str
    as_of: date
    decision: QualificationDecision
    qualification_required: bool | None
    foreign_filing_required: bool | None
    registered_agent_required: bool | None
    registered_agent_appointment_required: bool | None
    domestic_reinstatement_required: bool
    filing_blockers: tuple[str, ...]
    reasons: tuple[str, ...]
    remedies: tuple[str, ...]
    entity_requirement: EntityRequirement
    sources: tuple[LegalSource, ...]
    rule_version: str
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComplianceAudit:
    entity: Entity
    target_state: str
    presence: BusinessPresence
    is_qualified: bool = False
    registered_agent: RegisteredAgent | None = None
    as_of: date | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_state", normalize_state(self.target_state))
        if not isinstance(self.entity, Entity) or not isinstance(self.presence, BusinessPresence):
            raise ValueError("Audit requires an Entity and BusinessPresence")
        if type(self.is_qualified) is not bool:
            raise ValueError("is_qualified must be boolean")
        if self.registered_agent is not None and not isinstance(
            self.registered_agent, RegisteredAgent
        ):
            raise ValueError("registered_agent must be RegisteredAgent or None")
        if self.as_of is not None and type(self.as_of) is not date:
            raise ValueError("as_of must be a date")
        if self.as_of is not None and self.entity.formation_date > self.as_of:
            raise ValueError("Audit date precedes formation")

    def evaluate(self, registry: "RulesRegistry | None" = None) -> AuditResult:
        if registry is None:
            from ..rules.registry import DEFAULT_REGISTRY

            registry = DEFAULT_REGISTRY
        state_rule = registry.get(self.target_state)
        rule = state_rule.for_entity(self.entity.entity_type)
        today = self.as_of or date.today()
        if self.entity.formation_date > today:
            raise ValueError("Audit date precedes formation")
        reasons: list[str] = []
        if self.target_state == self.entity.domestic_state:
            decision = QualificationDecision.NOT_REQUIRED
            reasons.append("Target is the domestic state; foreign qualification does not apply.")
        else:
            triggered = self.presence.activities & rule.threshold.trigger_activities
            uncertain = self.presence.activities - rule.threshold.exempt_activities - triggered
            if Activity.ISOLATED_TRANSACTION in uncertain:
                limit = rule.threshold.isolated_transaction_max_days
                duration = self.presence.isolated_transaction_days
                if (
                    rule.threshold.isolated_transaction_without_day_limit
                    and not self.presence.repeated_transactions
                ):
                    uncertain -= {Activity.ISOLATED_TRANSACTION}
                    reasons.append("Nonrepeated isolated transaction has no statutory day limit.")
                elif limit is not None and duration is not None:
                    if duration <= limit and not self.presence.repeated_transactions:
                        uncertain -= {Activity.ISOLATED_TRANSACTION}
                        reasons.append(
                            f"Isolated transaction meets the <= {limit}-day safe harbor."
                        )
                    else:
                        # Losing an exemption alone does not prove transacting business.
                        reasons.append(
                            "Transaction exceeds the isolated safe harbor or is repeated."
                        )
            if triggered:
                decision = QualificationDecision.REQUIRED
                reasons.append(
                    "Local operating activities trigger qualification screening: "
                    + ", ".join(sorted(a.value for a in triggered))
                    + "."
                )
            elif not self.presence.activities or uncertain:
                decision = QualificationDecision.REVIEW_REQUIRED
                reasons.append(
                    "More facts are needed to determine transacting business: "
                    + (", ".join(sorted(a.value for a in uncertain)) or "no activities supplied")
                    + "."
                )
            else:
                decision = QualificationDecision.NOT_REQUIRED
                reasons.append(
                    "Supplied activities fall within the encoded statutory safe harbors."
                )
        required = (
            None
            if decision == QualificationDecision.REVIEW_REQUIRED
            else decision == QualificationDecision.REQUIRED
        )
        domestic = self.target_state == self.entity.domestic_state
        filing = False if self.is_qualified or domestic else required
        agent_required = True if domestic or self.is_qualified else required
        if domestic:
            reasons.append(
                "Domestic registered-agent duties still apply without foreign qualification."
            )
        agent = self.registered_agent
        valid_agent = bool(
            agent
            and agent.state == self.target_state
            and (
                agent.is_physical_address
                or not state_rule.registered_agent.physical_in_state_address
            )
            and (not agent.is_po_box or state_rule.registered_agent.po_boxes_allowed)
        )
        appointment = None if agent_required is None else agent_required and not valid_agent
        reinstatement = self.entity.status != EntityStatus.GOOD_STANDING
        blockers: list[str] = []
        remedies: list[str] = []
        if reinstatement:
            remedies.append(
                "Resolve the domestic forfeiture/revocation and obtain current status evidence."
            )
            if filing is not False:
                blockers.append(
                    "Domestic status is forfeited/revoked; resolve it before foreign filing."
                )
        if filing:
            remedies.append("File " + "; ".join(f.name for f in rule.forms) + ".")
            remedies.append(rule.good_standing_evidence)
        if appointment:
            remedies.append("Appoint an eligible registered agent with a physical in-state office.")
        if decision == QualificationDecision.REVIEW_REQUIRED:
            remedies.append(
                "Review the actual local activity against the statutory transacting-business test."
            )
        warnings = [
            "This audit screens qualification, not sales-tax nexus or tax liability.",
            "Agent checks validate supplied address facts, not licensure or service availability.",
        ]
        if not state_rule.sources_verified:
            warnings.append(
                "Official sources have not been live verified; "
                "review statutes and fees before filing."
            )
        warnings.extend(state_rule.verification_issues)
        return AuditResult(
            entity=self.entity,
            target_state=self.target_state,
            as_of=today,
            decision=decision,
            qualification_required=required,
            foreign_filing_required=filing,
            registered_agent_required=agent_required,
            registered_agent_appointment_required=appointment,
            domestic_reinstatement_required=reinstatement,
            filing_blockers=tuple(blockers),
            reasons=tuple(reasons),
            remedies=tuple(remedies),
            entity_requirement=rule,
            sources=state_rule.sources,
            rule_version=state_rule.version,
            warnings=tuple(warnings),
        )
