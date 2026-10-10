# Wyoming source verification

Retrieved and reviewed **2026-10-10**, using the configured proxy and normal TLS
verification. [Response metadata and SHA-256 hashes](wyoming-evidence.json) record
each reviewed source. The official full [Title 17 PDF](https://wyoleg.gov/statutes/compress/title17.pdf)
was successfully fetched and read: SHA-256
`f0fd7eb843b83bb60095bad496330f8dfd46ff7051dff8d1bec822650a3671f6`.
Quotes below normalize PDF/HTML layout whitespace only.

## Qualification and sanctions

W.S. § 17-16-1501 requires corporate authority before transacting business and
lists safe harbors including internal affairs, bank accounts, out-of-state order
acceptance, interstate commerce, ownership of property without more, and an
isolated transaction completed within 30 days that is not part of repeated
transactions. W.S. § 17-29-114 applies the corporate provisions to foreign LLCs.

Foreign LP registration is required under § 17-14-1002. The engine conservatively
does not assume every corporate safe harbor also applies to an LP; unspecified
LP bank/internal/solicitation/isolated activity continues to require review.

W.S. § 17-16-1502(d) states:

> [Liability includes] all fees and license taxes, plus interest of eighteen
> percent (18%) ... and in addition ... a penalty in the amount of five thousand
> dollars ($5,000.00), reasonable audit expenses and reasonable attorney fees.

The same provision permits withholding the authority certificate until payment.
The corporate rule is applicable to LLCs through §§ 17-29-114 and 17-29-211 and
to LP penalties through § 17-14-1007(e). The model therefore calculates a
**single $5,000 component** and flags historical fees, license taxes, 18% interest,
audit and attorney costs as unresolved. It does not repeat $5,000 each year or
invent compound-interest accrual.

Corporate § 17-16-1502 and LP § 17-14-1007 prohibit maintaining proceedings until
qualification/registration while preserving contractual acts and defenses.
Foreign authority revocation is a Wyoming event, not a change to domestic-state
standing.

## Forms, current filing fees and status evidence

The [official fee schedule](https://sos.wyo.gov/Business/docs/BusinessFees.pdf)
is **effective July 1, 2026**, revised June 2026. It lists foreign corporation
Certificate of Authority, foreign LLC Certificate of Authority and foreign LP
Certificate of Registration at **$150 each**.

This corrected the original LP $100 value, derived from an old independent
snapshot. Current W.S. § 17-14-209(a)(v) expressly states:

> For registering a foreign limited partnership, a fee of one hundred fifty
> dollars ($150.00).

Each official application independently confirms the fee:

- [Foreign corporation](https://sos.wyo.gov/Forms/Business/FPROF/FP-CertificateAuthority.pdf)
- [Foreign LLC](https://sos.wyo.gov/Forms/Business/FLLC/FLLC-CertificateAuthority.pdf)
- [Foreign LP](https://sos.wyo.gov/Forms/Business/FLP/FLP-CertificateRegistration.pdf)

All three instructions require an original domestic-jurisdiction certificate of
existence/good standing **issued no more than 60 days before Wyoming filing**.
Each form includes the registered-agent consent attachment. Restore domestic
existence/authority before preparing these statements and attachments.

## Registered agent

W.S. § 17-28-101 requires a Wyoming street address that is a physical location
where the agent or an authorized natural person is physically present to receive
process. Individual agents must be at least 18 and resident in Wyoming. Each
reviewed entity application explains:

> The registered agent must have a physical address in Wyoming. ... A Drop Box
> is not acceptable. A PO Box is acceptable if listed in addition to a physical
> address.

Initial designation and consent are included in the qualification application;
the forms specify no additional initial agent-designation charge. The current
fee schedule separately prices a **later Appointment of New Registered Agent and
Office at $5**, information updates at $5 per affected entity and resignations at
$5 per affected entity. The commercial agent's own annual registration is **$50**,
which is a provider obligation, not the client's qualification fee. Private
agent service charges are outside the statutory schedule.

## Annual reports, tax formula and revocation

Corporate § 17-16-1630 and LLC § 17-29-209 confirm **the greater of $60 or
0.0002 of Wyoming capital/property/assets**, with statutory valuation and
exclusions. LP § 17-14-209(b) incorporates the corporate tax provisions. The
obsolete $50 floor in the historical mirror has been superseded.

The [official business FAQ](https://sos.wyo.gov/faqs.aspx?root=BUS) states that
foreign and domestic corporations, LLCs and LPs use the same license-tax formula.
Its anniversary example is:

> [If] your business registers or qualifies on January 15th, your annual report
> due date will be January 1st of each year.

Reports can be filed up to 120 days early. The corporate statute describes the
month of registration; the LLC statute uses month of organization. The engine
therefore refers to the actual Wyoming SOS record's anniversary month and due
date, supported by the FAQ's registration/qualification example, rather than
calculating it from the entity's home-state formation date alone.

The FAQ warns:

> [If] the annual report is not filed within sixty (60) days following the due
> date, the entity will be administratively dissolved.

For a foreign corporation, § 17-16-1531 also requires notice and allows 60 days
after perfected service to cure before revocation. These procedural conditions
are preserved, and neither a calculated balance nor a missed date automatically
mutates entity status. Reinstatement within two years may be available subject
to filing history, the statutory conditions, arrears and the applicable fees.

Online annual reports may incur a separate payment-processor convenience fee;
the FAQ says reports with fees above $500 cannot be e-filed. The annual amount
remains unquantified in the model until asset inputs are supplied.

## Filing processing windows

All three official application instructions state:

> Processing time is up to 15 business days following the date of receipt in
> our office.
>
> Wyoming statutes do not allow for expedited filing at this time.

The business FAQ states foreign authority/continuance/domestication filings are
mailed, reviewed in receipt order, with a maximum of 15 business days. Immediate
activation of certain domestic online formations does not apply to these foreign
applications. The model records the specific official window and absence of
expedited options, instead of a generic estimate in weeks.

## Coverage and limitations

All formal Wyoming `LegalSource` entries now refer to successfully fetched and
reviewed official publications and have review date 2026-10-10. The old independent
Title 17 mirror was historical corroboration only and was removed from formal
current sources. Fee/cycle/agent/sanction facts are now corroborated directly;
fact-dependent tax balances, interest timing, legal-service expenses and the
ultimate legal finding of transacting business are not calculated from missing
inputs. This verification does not guarantee future statutory or fee stability.
