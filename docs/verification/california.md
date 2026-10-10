# California source verification

Review/retrieval date: **2026-10-10**. The sources below were fetched through the
configured proxy with TLS verification enabled, returned HTTP 200, and their
relevant text was read. SHA-256 values identify the original response bytes,
before HTML text extraction. Quoted text normalizes layout whitespace only.
The citations in `REQUIREMENT.sources` distinguish reviewed official agency pages
from legislative URLs whose `verified_on` is still `None`.

## Forms, fees and reports

| Official source | SHA-256 of response bytes |
| --- | --- |
| [SOS foreign corporation forms](https://www.sos.ca.gov/business-programs/business-entities/forms/corporations-foreign-out-state-or-out-country) | `a2b58827e6c068836dc32ecf90038ae3910a5059ee94522e288a1a0612580d6b` |
| [SOS foreign LLC forms](https://www.sos.ca.gov/business-programs/business-entities/forms/limited-liability-companies-foreign-out-state-or-out-country) | `86bb71f931bc964aca8df30dc189f3cae360a2eec3f69137ca70d3646d8a4aac` |
| [SOS foreign LP forms](https://www.sos.ca.gov/business-programs/business-entities/forms/limited-partnership-foreign-out-state-or-out-country) | `bf664a177a7065f0de15fc2fdff651bf567a346571003aba8f2ba0c94b50cdc4` |
| [SOS Statement of Information filing tips](https://www.sos.ca.gov/business-programs/business-entities/statements) | `3059bd4107e9f2b1b1cec0c28e33962f14e149301b63cb6c112df8f28b93b4aa` |

The foreign corporation table lists these cells together:

> Statement and Designation by Foreign Corporation - Stock
> Form S&DC-S/N (PDF)
> $100.00

The LLC table lists “Application to Register”, “Form LLC-5 (PDF)”, and “$70.00”.
The LP table lists “Application for Registration”, “Form LP-5 (PDF)”, and “$70.00”.
The fees match the module's base qualification fees; service charges and taxes
remain separate.

The corporation report row states:

> Statement of Information - Foreign Stock: Due within 90 days of initial
> registration and every year thereafter.

That row identifies **SI-550, $25.00**. The LLC report row states:

> Statement of Information: Due within 90 days of initial registration and every
> two years thereafter.

That row identifies **LLC-12, $20.00**. The LP forms table has no recurring
Statement of Information row; this corroborates the existing absence of a routine
SOS annual report in the LP model, but is not a replacement for statutory review.

The statement filing tips page labels its schedule:

> Statutory Required 6 Month Filing Window

For a January registration month its table reads **January / August / January**
under registration month / first day of / through last day of. For October it
reads **October / May / October**. The complete twelve-row table confirms the
anniversary month and preceding five months encoded by the model.

The same page announces that, effective August 1, 2026, user access is required
for online Statement of Information filings. A requirement output does not itself
provide that filing authority or portal access.

## Qualification, agents and forfeiture

[SOS business entity FAQs](https://www.sos.ca.gov/business-programs/business-entities/faqs)
returned SHA-256
`a1fbff2d58902ba716dbcf749346804c3c675314f58c7ec7c73e8afdcd1d4cd5`.

> Before transacting intrastate business in California, the business must first
> qualify/register with the California Secretary of State online at
> bizfileOnline.sos.ca.gov. "Transacting intrastate business" is defined as entering
> into repeated and successive transactions of its business in this state, other
> than interstate or foreign commerce.

This confirms the general screening test. The FAQ links Corp. Code §§ 191, 2105,
15909.02, 17708.02 and 17708.03. It does **not** independently establish every
safe harbor, the 180-day exception, or the LP income-producing-property rule.

The qualification instructions say a corporation must attach a valid certificate
of good standing issued by an authorized public official of its formation
jurisdiction. They similarly require a valid certificate for the LLC, and a
certificate “(or other record of similar import)” for the LP. Specific six-month
certificate ages in the model still depend on the unverified statutes.

> An agent for service of process is an individual who resides in California, or a
> registered 1505 corporate agent, designated to accept service of process (court
> papers) if the business entity is sued.

> The individual agent should be aware that the name and the physical street
> address of the agent for service of process is a public record, open to all

> A business entity cannot act as its own agent for service of process

The FAQ also requires a corporate agent to be active and have a current 1505
application on file. Address validation alone does not verify these eligibility
facts.

The FAQ distinguishes delinquency certification for a penalty from a pending
suspension/forfeiture notice:

> If the statement has not been filed timely, the entity is provided a notice of
> delinquency, and after 60 days from that notice, if no statement has been filed,
> the Secretary of State’s office notifies the Franchise Tax Board, who assesses
> and collects the penalty.

> the Statement of Information must be received and filed by the California
> Secretary of State no later than 60 days from the Notice Date that appears on the
> Notice of Pending Suspension/ Forfeiture.

The late penalty is therefore not an automatic assessment 60 days after the
original report due date. Model estimates require the notice date; they also
remain conditional on SOS certification and applicable relief. California
forfeiture does not alter the domestic jurisdiction's status automatically.

## Penalty and tax guidance

| Official source | SHA-256 of response bytes |
| --- | --- |
| [FTB penalty reference chart](https://www.ftb.ca.gov/forms/misc/1024.html) | `6b027b3cffb75c81fc4a3e3d6a7cbdd1cbd41bf9dbbf7f2a0fca638935e34040` |
| [FTB common penalties](https://www.ftb.ca.gov/pay/penalties-and-interest/index.html) | `4a7c2a6cc8e5a4263ac6fc7137fca49d35069691bbd2880876543e9426b26dc8` |
| [FTB suspension and revival](https://www.ftb.ca.gov/help/business/my-business-is-suspended.html) | `6a3c1cc432cae5eafc47ccefd46f1ffd5db96f5fc9b2f2d12741aa2d9eea5642` |
| [FTB LLC tax guidance](https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html) | `5064e3b6566be374bc9e4584257920ded5533e99d43bcf349ea387db5a3f5591` |
| [FTB doing-business tax test](https://www.ftb.ca.gov/file/business/doing-business-in-california.html) | `40561b6ed2649857169124c92ba6967a8465ee32ac3609225b08a5eefc07409a` |

The reference chart's R&TC § 19135 row states:

> Any foreign corporation which fails to qualify to do business, or whose powers
> have been forfeited, or any domestic corporation which has been suspended, and is
> doing business in this state, within the meaning of Section 23101, and fails to
> make and file a return within 60 days of FTB’s notice and demand.

It lists **“$2,000 per taxable year.”** and relief for **“Reasonable cause and not
willful neglect.”** This is a separate demanded-tax-return sanction; it is not
the corporate daily qualification penalty. The agency chart uses corporate tax
terminology; LLC applicability must account for tax classification and governing
definitions before assigning a monetary liability.

The chart's R&TC § 19141 row states:

> Upon certification by the Secretary of State, penalty for taxpayer’s failure to
> provide a Statement of Information.

It lists **“$250 upon certification by the Secretary of State under Corporations
Code Sections 2204 and 17653.”** The reference to the former LLC section 17653 is
on the agency chart; current LLC statutory citations in the module remain
unverified. The common-penalties page independently lists **“All other businesses:
$250”** for the SOS Statement of Information penalty and notes that only SOS can
waive it.

The suspension guidance states:

> When your business has been suspended or forfeited, it is not in good standing
> and loses its rights, powers, and privileges to do business in California.

It requires past-due tax returns, past-due tax balances and a revivor request to
restore FTB good standing; simultaneous SOS and FTB suspensions can require both
sets of remedies.

LLC tax guidance states:

> Your subsequent annual tax payments will continue to be due on the 15th day of
> the 4th month of your taxable year.

The tax doing-business page lists transactions for financial gain, commercial
domicile and sales/property/payroll thresholds. These are tax tests and do not
replace the qualification test. The module deliberately does not calculate a
universal annual tax amount.

## Processing queues and optional service charges

[SOS service options](https://www.sos.ca.gov/business-programs/business-entities/service-options)
returned SHA-256
`f150225103dffef4f7f96f0d687131a937662514e70fa0d093d497a2e8262b65`.

> 24–Hour Filing Service (Class C) - $350.00: Online or Drop-Off in Sacramento.

The subsequent sentence guarantees a filing response within 24 hours, excluding
weekends and holidays. Same-day service is **$750**:

> the document must be received by the Secretary of State by 9:30 a.m., and a
> filing confirmation or filing response will be available the same day by
> 4:00 p.m.

Those are California local times, not the chat client's timezone. The **$500
four-hour service** is Sacramento drop-off only and requires approved
preclearance. A separate **$500 24-hour preclearance service** excludes weekends
and state holidays. These services promise a response; rejection is possible.

> $15 special handling fee is applicable for each filing request.

The page explicitly excludes Statements of Information, Statements by Common
Interest Development Association and requests submitted online/by mail from the
handling fee. It says handling charges are additional and retained on rejection.
Optional services are not included in `filing_fee`.

[SOS current processing dates](https://www.sos.ca.gov/business-programs/business-entities/processing-dates/)
returned SHA-256
`7da068fc55b69be36252944817bced19b750bd2589f0c213410cef31aed48ef5`.

> Last updated: October 9, 2026

> Processing dates vary depending on the type of request submitted, how the
> request is submitted, and when the request is received by the California
> Secretary of State's office.

The corporation, LLC and LP tables each say the office is reviewing
**Formations/Registrations** received online **10/07/2026**, in person
**10/06/2026**, and by mail **10/05/2026**. These are a dated queue snapshot, not a
service guarantee or a general fixed turnaround calculation. Consult the live
page to schedule a filing.

## Unverified primary-law coverage

On 2026-10-10 the official [Corp. Code § 2203 section endpoint](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CORP&sectionNum=2203.)
returned HTTP 403. Supported full-chapter endpoints for [chapter 21](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CORP&division=1.&title=1.&part=&chapter=21.&article=)
and [chapter 22](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CORP&division=1.&title=1.&part=&chapter=22.&article=)
also returned HTTP 403. No denied response is treated as verified source text,
and no direct-connection or TLS bypass was used. Other legislative section URLs
in the module remain unverified; the representative failures are not evidence
that their legal content was read.

Outstanding primary-law checks include the **court-assessed corporate $20 per
willful-business day**, the **LP $20 per day capped at $10,000**, the LLC's distinct
enforcement provisions, safe-harbor details, certificate ages, and current fee
statute subsection numbering. Consequently `REQUIREMENT.sources_verified` remains
false even though official agency guidance and fee tables were reviewed live.

Historical implementation context: before official agency pages became
accessible, statute text was compared with an [independent legislative bulk-data
mirror pinned at commit d1cfd8b](https://github.com/johnakelly-yahoo-com/california-codes/tree/d1cfd8b5d5970f52f403e4a986cad06281169acd/codes).
That mirror is not an official source, was not live primary-law verification, and
has been removed from the formal `LegalSource` collection. No claimed future tax
amendment from that mirror is used to assign a universal tax obligation.
