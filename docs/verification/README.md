# State rule source verification

Latest batch review date: **2026-10-11** (original five states: October 10).

[Batch nine](batch9-2026-10-11.md) adds Vermont, Virginia, West Virginia and
Wisconsin: **49 populated states**, one coming-soon state (Maryland), and eight
new LLC/C-Corp guides. [Retrieval records](batch9-2026-10-11-retrievals.json)
document official legislative and operational evidence, including Virginia's
disclosed annual corporate fee discrepancy and West Virginia's July 2026
conditional biennial election. Variable or conflicting assessments remain manual.

The user accepted Tennessee's Justia statutory citations as sufficient review;
its primary-review flag is now satisfied. [Batch eight](batch8-2026-10-11.md) and
its [retrieval records](batch8-2026-10-11-retrievals.json) preserve the acceptance
and secondary-source classification. Acceptance does not relabel Justia as an
official statutory publisher.

The original-state table and baseline discussion below are historical; subsequent
batch/review logs and current rule flags record later conflict resolutions.
The [next-batch evidence](batch-2026-10-11.md) covers Georgia, Illinois, New York,
North Carolina, and Washington, including open review issues.
A source is reviewed only after relevant
official content has been retrieved and read. A successful HTTP status, a
JavaScript application shell, a challenge page, or an independent historical
mirror does not establish live statutory or operational verification.

| State | Review status | Evidence and remaining issues |
| --- | --- | --- |
| Wyoming | All listed official sources reviewed; no recorded verification issues. | [Wyoming evidence](wyoming.md): statutes, foreign forms, filing fees, agent duties, annual license tax/report, and processing instructions. |
| Texas | All listed official sources reviewed; no recorded verification issues. | [Texas evidence](texas.md): current official legislative backend, SOS forms/fees/expedited guidance, and Comptroller tax/report instructions. |
| Delaware | All listed official sources reviewed; one unresolved official conflict. | [Delaware evidence](delaware.md): foreign corporate annual-report late penalty is $200 in the statute and $250 in SOS guidance. Current foreign forms and August 2026 fees were read. |
| California | Agency review complete for listed accessible guidance; primary-law review incomplete. | [California evidence](california.md): SOS and FTB guidance reviewed, while official legislative source sections returned HTTP 403. |
| Florida | Official 2026 legislative chapters reviewed; operational review incomplete. | [Florida evidence](florida.md): DOS form/report pages returned origin challenges; actual forms, expedited availability, and processing windows remain unverified. |

Each state document records reviewed claims, source URLs, response hashes or
retrieval evidence, and concrete limits. Earlier failures and independent mirrors
are retained as historical context where relevant, rather than counted as current
official review. Texas and Wyoming also retain machine-readable retrieval evidence
in their adjacent JSON files.

In the model, `LegalSource.verified_on` records content review;
`StateRequirement.sources_verified` requires review dates for every listed source.
`StateRequirement.rules_verified` additionally requires an empty
`verification_issues` tuple. Thus Delaware's sources are reviewed while its rule
set retains a conflict. California and Florida retain unset dates for unreviewed
sources. Audit warnings and generated jurisdiction guides carry those gaps and
conflicts forward.

Review dates describe the repository's source snapshot, not certification that a
future filing will be accepted. Recheck official instructions and resolve any
applicable open issue before relying on a filing amount, deadline, or eligibility
condition.
