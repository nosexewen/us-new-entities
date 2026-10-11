# Florida rule verification

**Follow-up:** [October 11 evidence review](review-2026-10-11.md) resolves
California/Florida retrieval gaps and Illinois/New York/North Carolina/Washington
flags. Georgia and Delaware retain documented issues. Findings below record the
earlier review history.

Reviewed on 2026-10-10 against the official live **2026 Florida Statutes**, chapters 605, 607, and 620. Relevant source content was read; the successful HTTP responses alone were not treated as proof. The earlier 2025 independent PDF mirror is historical provenance only.

## Verified statutory findings

| Type | Foreign application government fee | Registered-agent designation government fee | Total initial state filing fee | Annual report government fee | Supplemental corporate fee | Annual total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LLC | $100 | $25 | $125 | $50 | $88.75 | $138.75 |
| C-Corp | $35 | $35 | $70 | $61.25 | $88.75 | $150 |
| LP | $965 | $35 | $1,000 | $411.25 | $88.75 | $500 |

Sources: §§ 605.0213(3), (5), (7); 607.0122(5), (14), (17); 620.1109(3), (7), (8)(a); 607.193(1). These government charges do not set an agent's separate private service price.

- **Qualification:** §§ 605.0902, 607.1501–607.1503, 620.1902 require foreign authorization before transacting local business. Normal intrastate operations are screening signals, not a substitute for factual legal review.
- **Safe harbors:** §§ 605.0905, 607.1501(2), 620.1903 include bank accounts/internal affairs, interstate commerce, and orders requiring acceptance outside Florida. Isolated transactions must be completed within 30 days and outside repeated/similar transactions. Bare property ownership is treated separately from productive local business.
- **Income-producing property (LLC/LP):** §§ 605.0905(3), 620.1903(3) say ownership of income-producing real or tangible personal property, other than listed exceptions, “constitutes transacting business.” Explicit productive-property activity is a trigger with exception notes; unspecified property remains a review case.
- **LLC qualification sanction:** § 605.0904(7) says “at least $500 but not more than $1,000 for each year or part thereof,” plus unpaid fees/penalties. **Corporation** § 607.1502(4) states the same range but only “to the extent ordered by a court of competent jurisdiction.” Year-period estimates use anniversary counting, with the collecting authority to confirm the assessment basis. **LP** § 620.1907 has no equivalent annual $500–$1,000 schedule; litigation is barred until authorized and § 620.1908 permits Attorney General restraint. Unknown monetary remedies are not modeled as zero.
- **Existence evidence:** §§ 605.0902(2), 607.1503(2), 620.1902(2) require official domestic existence evidence authenticated “not more than 90 days” before delivery. § 620.1902(1)(e) additionally requires nonindividual general partners to be registered as required and active, not dissolved/revoked/withdrawn.
- **Agent and address:** §§ 605.0113, 607.1507, 620.1114 require an eligible Florida resident individual or authorized person/entity and in-state registered office; application provisions expressly request a Florida street address and written agent acceptance. Registered-office/agent address must match. A postal box alone is not the street address requirement. For LLC/corporation, missing-agent compliance can separately produce a court-ordered $5/day penalty capped at $500 (§§ 605.0113(5), 607.1507(6)); this is not the qualification sanction.
- **Annual reports:** §§ 605.0212(3), 607.1622(4), 620.1210(3) say the first report is January 1–May 1 of the year following authorization, then annually in that window.
- **Late annual fee:** § 607.193(2)(b) says “a late charge of $400 shall be imposed if the supplemental corporate fee is remitted after May 1,” with an exception for entities revoked/dissolved for annual-report failure that then reinstate and pay the applicable reinstatement fee. This applies to all three annual-report chapters, including LP, and is not a compounded monthly fee.
- **Foreign report revocation:** §§ 605.0908(1)(a), (2), 607.1530(1)(a), (2), 620.1906(1)(b), (2) state the report must arrive by 5 p.m. Eastern on the third Friday in September, then revocation for missing report occurs on the fourth Friday. Other revocation grounds/processes remain separate.
- **LP reinstatement:** § 620.1109(6) says “$500 for each calendar year or part thereof” administratively dissolved/revoked. This does not become an annual unqualified-business sanction.

## Forms and processing remain unresolved

The model includes descriptive foreign application form names and official SOS form landing pages. Actual current form PDFs and operational fee/annual-report instructions have **not** been read: `https://dos.fl.gov/sunbiz/forms/`, the LLC forms/fee pages, and annual-report page returned an origin **Cloudflare challenge (`cf-mitigated: challenge`)**, not a destination-policy denial. `files.floridados.gov` was reachable with an ordinary browser user agent but a guessed legacy form path was a genuine 404; no PDF contents were verified. No secret or authentication value was requested.

Because actual SOS operational guidance remains blocked, `verified_on` remains unset for the SOS form and annual-report sources. `verification_issues` also records unreviewed expedited availability and processing windows. No optional expedited fee, normal turnaround, or operational guarantee is invented from the statutes. Source-specific verification is retained for the successfully read 2026 legislative chapters; that does not imply fully verified filing instructions.

## Reviewed-source retrieval evidence

Hashes cover the full original HTML response bytes, before text normalization. All traffic used the environment HTTPS proxy with TLS verification enabled.

| Reviewed official source | Retrieved at (UTC) | SHA-256 of retrieved bytes |
| --- | --- | --- |
| [fl_llc](https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0605/0605.html) | 2026-10-10T04:21:03.066716+00:00 | `dece330e19122d0fe2e95f735cf1d6bd1bb0d61e8a4d89bee6cce83d2a240416` |
| [fl_corp](https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0607/0607.html) | 2026-10-10T04:21:03.067319+00:00 | `0e124c9ab6036716a1ba11f13e6daa07b87ed714b0351f693678bf5d0a4b9441` |
| [fl_lp](https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0620/0620.html) | 2026-10-10T04:21:03.067827+00:00 | `e78fc5f10cce70e5dbf7f28cb6e0eca8ed5f6ec55b5057b731d5c8dd52e78c92` |
