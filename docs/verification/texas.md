# Texas source verification

Retrieved and reviewed **2026-10-10**, using the configured proxy and normal TLS
verification. [Response metadata and SHA-256 hashes](texas-evidence.json) identify
each reviewed original HTML/PDF response. Quotes below normalize whitespace only.
The statutory website's JavaScript shell was not counted as statutory verification.
After the document backend was added to the published network policy, actual
statute text was fetched and reviewed successfully. **All 18 formal sources are
reviewed; no Texas source-access verification issues remain.**

## Qualification, fees and penalties

The [SOS foreign-entity FAQ](https://www.sos.state.tx.us/corp/foreignfaqs.shtml)
explains that Texas statutes do not specifically define transacting business,
that BOC § 9.251 contains excluded activities, and that offices, employees and
pursuing an entity purpose are general screening indicators. The engine retains
review for employees whose duties are unspecified, rather than classifying every
employee as a definitive trigger. Corporate/LLC/LP qualification forms are
[301](https://www.sos.state.tx.us/corp/forms/301_boc.pdf),
[304](https://www.sos.state.tx.us/corp/forms/304_boc.pdf) and
[306](https://www.sos.state.tx.us/corp/forms/306_boc.pdf).

The [official fee schedule](https://www.sos.state.tx.us/corp/forms/806_boc.pdf),
revised September 2026, lists **$750** for these foreign registrations. It states:

> A foreign entity that has transacted business in Texas for more than ninety
> days without registering is subject to a late filing fee. The late filing fee
> is equal to the registration fee for each full or partial calendar year that
> the foreign entity transacted business in Texas without being registered.

The FAQ expressly multiplies **whole or partial calendar years since the initial
transaction date**, not merely years after day 90. Its example is June 1, 2007
through registration December 1, 2010: $3,000 late fees plus $750 registration.
The engine retains this calendar-year/grace policy. Actual [BOC Chapter 9](https://tcss.legis.texas.gov/resources/BO/htm/BO.9.htm)
text confirms § 9.054 authorizes the SOS to collect the fee and condition
registration on payment.

Review of **§ 9.251** confirmed interstate commerce, bank accounts and internal
affairs safe harbors, and an isolated transaction completed within 30 days that
is not part of repeated similar transactions. It also corrected an inherited
model error: **out-of-state order acceptance is not an enumerated Texas
exemption**. `Activity.SOLICITATION` alone now needs review; separately established
interstate-only commerce remains exempt. Section 9.252 makes the list nonexclusive,
so the engine does not convert an unlisted activity into an automatic violation.
Other listed exemptions, including owning property "without more," require more
precise facts than the model's unspecified property activity.

[Form 304 instructions](https://www.sos.state.tx.us/corp/instructions/304.shtml)
separately state:

> [An unregistered entity] is subject to a civil penalty in an amount equal to
> all fees and taxes that would have been imposed if the entity had registered
> when first required.

They also describe injunction and inability to maintain proceedings until
registered. The $750-per-year estimate is therefore a **late registration fee
component**, not a complete civil/tax liability quote. Historical tax/filing facts
remain unresolved, including during the 90-day late-fee exemption.
The primary statute § 9.052 expressly adds:

> penalties and interest imposed by law for failure to pay those fees and taxes.

Those components are retained as unresolved historical civil exposure, rather
than omitted or added to the $750 calendar-year amount using invented rates.

The form requires a statement that the entity exists validly in its domestic
jurisdiction and is authorized there to pursue its proposed Texas activity.
The standard reviewed forms do not require attaching a home-state status
certificate. The model nevertheless requires restoration of a forfeited/revoked
domestic entity before treating its registration application as ready.

## Registered agent

The [SOS registered-agent FAQ](https://www.sos.state.tx.us/corp/registeredagentfaqs.shtml)
and Form 304 instructions confirm a consenting individual Texas resident or
eligible registered/authorized organization; an entity cannot be its own agent.
Form 304 instructions state:

> The registered office address must be located at a street address where service
> of process may be personally served on the entity's registered agent during
> normal business hours.

The office cannot consist solely of a mailbox or answering service. Consent is
required but **normally retained by the entity, not separately filed**. The FAQ
prices optional separate filing of consent at **$15** for these entity types.
Initial designation is already part of the $750 application; private service
charges are not SOS filing fees.
Primary [BOC Chapter 5](https://tcss.legis.texas.gov/resources/BO/htm/BO.5.htm)
§§ 5.201–5.2011 independently confirm the continuous designation, resident or
eligible organizational agent, written/electronic consent, street address and
mailbox/answering-service restrictions.

## Annual and periodic reporting

The [Comptroller franchise-tax page](https://comptroller.texas.gov/taxes/franchise/)
states that the annual report is due **May 15**, moved to the next business day
when it falls on a weekend/holiday. Its sanctions section states:

> A $50 penalty is assessed on each report filed after the due date.
>
> If tax is paid 1-30 days after the due date, a 5 percent penalty is assessed.
>
> If tax is paid over 30 days after the due date, a 10 percent penalty is assessed.
>
> Past due taxes are charged interest beginning 61 days after the due date.

The model estimates only the $50 late-report component and keeps unpaid-tax
percentages, interest and relief dependent on tax-account facts. Neither the
franchise tax amount nor its nexus test is inferred from foreign qualification.
Primary [Tax Code Chapter 171](https://tcss.legis.texas.gov/resources/TX/htm/TX.171.htm)
§ 171.362 confirms the $50 applies even when no tax is due or a report is later
filed. Subsections (a)–(c) apply 5% of tax due for late payment/reporting, another
5% after 30 days, and a $1 minimum for these percentage penalties. The $50 modeled
component does not include that minimum or the tax percentages.
[Tax Code Chapter 111](https://tcss.legis.texas.gov/resources/TX/htm/TX.111.htm)
§ 111.060(c) says delinquent taxes draw interest "beginning 60 days after the date
due"; the Comptroller describes its operational convention as beginning 61 days
after the due date. The annual rate for post-1999 report periods is variable,
prime plus one percent under § 111.060(b), so no fixed or compounded interest
amount is inferred from the qualification interval.

The [PIR/OIR requirements](https://comptroller.texas.gov/taxes/franchise/pir-oir-filing-req.php)
corrected a material initial-model error: **taxable LPs file a Public Information
Report (PIR), just as corporations and LLCs do**. OIR is for other taxable entity
types. The page also states that PIR/OIR can remain due below the no-tax-due
threshold, while tax-exempt, qualifying passive and qualifying new veteran-owned
entities have exemptions. Failure can cause tax forfeiture and consequences for
proceedings and certain personal debt liabilities; this is separate from missing
qualification and does not change home-state standing.
Primary §§ 171.251, 171.2515 and 171.256 confirm **45 days after mailed/electronic
notice** to cure report, tax or penalty defaults before tax forfeiture. The
Comptroller may apply the same procedures to noncorporate taxable entities.
Tax forfeiture proceedings restrictions under § 171.252 differ from foreign
qualification restrictions; one must not infer preserved tax litigation rights
from the right to defend under BOC § 9.051.

The SOS FAQ and [Form 804 instructions](https://www.sos.state.tx.us/corp/instructions/804.shtml)
also support an **LP periodic SOS report when requested**, not more than once in
four years. Primary [BOC Chapter 153](https://tcss.legis.texas.gov/resources/BO/htm/BO.153.htm)
§ 153.301 precisely limits this to LPs **not required to file a PIR under Tax Code
§ 171.203**; the SOS must require the report. Determine applicability from those
requirements and the SOS notice.
The base fee is **$50**. After failure to file within 30 days of first notice:

> [The] fee is the original $50 plus a late fee of $25 per month or part of a
> month for one hundred twenty (120) days following the forfeiture
> (maximum late fee $100).

Instructions describe revocation after 120 days from the second notification and
reinstatement with a **$225** filing total ($50 report, $100 late fee, $75
reinstatement) and Comptroller tax clearance. These values are included as a
conditional LP obligation; the monthly estimate starts at forfeiture.
Primary §§ 153.304, 153.307–153.311 establish that the report is due by the 30th
day after the initial notice is mailed, failure forfeits Texas business rights
without a court determination, a forfeiture notice follows, and revival requires
the report and fees by the 120th day after mailing that forfeiture notice. The SOS
may revoke an unrevived foreign LP registration; it is not an automatic annual
forfeiture triggered by formation-date anniversaries.

For existing foreign registrations generally, BOC § 9.101 authorizes SOS
revocation when report/fee/penalty, agent/office or amendment defaults remain
uncorrected **before the 91st day after mailed notice**. Unpaid or dishonored
initial registration fees use **the 16th day**. These are notice-based cure
periods, not permission for unregistered entities to conduct business. Sections
9.103–9.104 require correction and reinstatement filing by the third anniversary
of revocation, tax clearance for taxable entities, and separate procedures for
Tax Code forfeiture or court termination.

## Processing and optional costs

[Texas Express](https://www.sos.state.tx.us/express.shtml) and the September 2026
fee schedule confirm these **additional per-document** options:

| Option | Additional fee | Official service window |
| --- | ---: | --- |
| Standard expedited | $50 | Typically 2–3 business days; processed before regular submissions |
| Next-day | $500 | Received by noon Central, processed by next business day's close |
| Same-day | $750 | Received by noon Central, processed by same business day's close |
| Preclearance | $50 | Draft review; no fixed turnaround stated on the reviewed page |

Same/next-day requests use SOSPortal or in-person service; standard expedite also
allows mail. No fixed ordinary-processing window was established in reviewed
guidance. These are official stated service conditions, not a guarantee for an
incomplete or noncompliant filing.

[Filing/payment options](https://www.sos.state.tx.us/corp/options.shtml) state that
portal credit-card payment adds **$0.25 per transaction plus 2.25%** of charged
fees; ACH and mailed check/money-order options are available. Optional processing,
payment and private-agent costs remain outside base statutory registration fees.

## Primary-law access history and resolution

The legacy BOC 5, BOC 9 and Tax Code 171 `.htm` routes, the BOC 9 PDF route,
`GetStatute.aspx`, and a supported `/resources/BO/htm/BO.9.htm` route all returned
the same 250,874-byte **Angular homepage**, SHA-256
`dbfba8a96dc3cd584157ca66aaafdf67e0ed15dd5a0c8a58f3d4bd0f109fc646`.
Those responses were not treated as legal text and are not the formal source
URLs now used by the Texas registry.

The official application's downloaded JavaScript specifies its current text API
and document backend as `https://tcss.legis.texas.gov/api/` and
`https://tcss.legis.texas.gov/resources`. At initial review that additional
official hostname was outside the published allowlist. No proxy bypass was used.
After the updated policy was published, the following supported official GET
routes returned actual statute text and relevant provisions were read:

- [BOC Chapter 9](https://tcss.legis.texas.gov/resources/BO/htm/BO.9.htm):
  §§ 9.001, 9.051–9.054, 9.101–9.104, 9.251–9.252.
- [BOC Chapter 5](https://tcss.legis.texas.gov/resources/BO/htm/BO.5.htm):
  §§ 5.201–5.206.
- [BOC Chapter 153](https://tcss.legis.texas.gov/resources/BO/htm/BO.153.htm):
  §§ 153.301–153.312.
- [Tax Code Chapter 171](https://tcss.legis.texas.gov/resources/TX/htm/TX.171.htm):
  §§ 171.202–171.203, 171.251–171.258, 171.362.
- [Tax Code Chapter 111](https://tcss.legis.texas.gov/resources/TX/htm/TX.111.htm):
  § 111.060.

Metadata and hashes are retained in the evidence file. Texas `sources_verified`
and `rules_verified` are now true for this reviewed rule version. Verification
records establish provenance and review dates, not a promise that future legal
changes cannot alter these requirements.
