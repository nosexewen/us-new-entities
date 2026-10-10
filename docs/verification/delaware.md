# Delaware rule verification

Reviewed on 2026-10-10. Verification means relevant source content was read, not merely that a URL returned HTTP 200. For statutes, the cited sections were reviewed in the official live HTML and/or official title PDF. These findings supersede the initial 2015 independent DGCL mirror.

## Current verified findings

- **Foreign LLC/LP annual tax is $400**, due June 1 for the preceding calendar year, with no annual report. The official SOS instruction says: “required to pay an annual tax of $400.00. There is no requirement to file an Annual Report.” The official text of 6 Del. C. §§ 18-1107(b), 17-1109(a) agrees. This corrects the initial $300 reference snapshot.
- **Late annual tax:** $200 added to tax, plus 1.5% for each month or portion thereof on unpaid tax and penalty. The SOS says “$200.00 plus 1.5% interest per month on tax and penalty.” §§ 18-1107(c), (e), 17-1109(b), (d) do not authorize interest on accrued interest. The calculator uses simple interest and excludes tax principal from the penalty total. Separate missed tax years require separate estimates.
- **Foreign registration lapses when annual tax is not paid when due:** §§ 18-1107(h), 17-1109(g) say a foreign entity “shall cease to be registered.” Payment restores registration under §§ 18-1107(i), 17-1109(h). Three-year cancellation of domestic certificates is a separate rule and is not a foreign-registration grace period. After three months in arrears, the Attorney General may seek an injunction under §§ 18-1107(j), 17-1109(i); this is discretionary, not automatic forfeiture.
- **LLC/LP unqualified-business sanction is $200 per year or part:** §§ 18-907(d), 17-907(d) say “shall be fined and shall pay to the Secretary of State $200 for each year or part thereof.” Fees/penalties from the unregistered period also must be paid before maintaining an action. The calculator's year counting uses anniversaries; the collecting authority must confirm the assessment basis.
- **Corporate unqualified-business sanction is per offense:** 8 Del. C. § 378 says “not less than $200 nor more than $500 for each such offense.” It is not a daily or monthly fine. Agents have a separate $100–$500 per-offense sanction. § 383 bars maintaining an action until qualification and arrears; contracts remain valid and defending an action remains possible.
- **Existence evidence applies to all three types:** §§ 371(b)(1), 18-902(2), 17-902(2) require a certificate issued “not earlier than 6 months prior to the filing date.” LLC/LP applications also require an authorized-person assertion of valid existence as of filing. This corrects the initial LLC/LP attachment guidance.
- **LLC/LP isolated-transaction exemption has no fixed day limit:** §§ 18-912(a)(10), 17-912(a)(10) cover an isolated transaction outside a course of similar transactions. The model uses `isolated_transaction_without_day_limit=True`. The corporate safe harbors in § 373 do not state this general exemption. Wholly interstate activities and specified outside-state accepted/fulfilled solicitation are protected; § 373(a)(2) includes offices used only for protected solicitation.
- **Physical in-state registered office/agent:** §§ 131(c), 132(b), 18-104, 18-904(b), 17-104, 17-904(b) require a Delaware registered office/eligible agent. § 131(c) says the address includes “street, number, city, county and postal code.” Agent offices must be available to accept service. A postal box alone does not satisfy these requirements.
- **LLC/LP base foreign filing fee is $200:** §§ 18-1105(a)(6), 17-1107(a)(6). Private registered-agent service pricing is not set by these government filing fees.
- **Foreign corporate annual report:** June 30, $250 filing fee under §§ 374, 391(a)(8). Failure to file within any two-year period terminates the right to do business under § 375. Foreign qualification alone does not impose the domestic corporate franchise-tax calculation.

## Unreconciled official conflict

Current 8 Del. C. § 391(a)(8) says: “the corporation shall pay a penalty of $200.” The current SOS [Annual Report and Tax Instructions](https://corp.delaware.gov/paytaxes/) says: “a $250.00 penalty will be added to filing fee.” Both sources were actually retrieved and reviewed. The model stores the statutory $200 amount with an unresolved component; `exact_amount` is unavailable and the state's `verification_issues` preserves the conflict. Obtain a confirmed assessment before operationally relying on the late amount. The report fee itself is consistently $250.

## Forms, fee components, and expedited processing

The live [foreign corporate form index](https://corp.delaware.gov/corpformsforcorp09/), [LLC form index](https://corp.delaware.gov/corpformsllc09/), and [LP form index](https://corp.delaware.gov/corpformslp09/) each list “Foreign Qualification” and link the actual official PDFs:

- [Foreign corporation](https://corpfiles.delaware.gov/Foreign_Corp/Foreign%20Corporation.pdf)
- [Foreign LLC](https://corpfiles.delaware.gov/LLC_Forms/Foreign%20LLC.pdf)
- [Foreign LP](https://corpfiles.delaware.gov/LP_Forms/Foreign%20LP.pdf)

The PDF instructions and [August 2026 Fee Schedule](https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf) were successfully retrieved and read at 05:47 UTC after the runtime's allowed domains changed. The earlier proxy CONNECT 403 is resolved. The schedule explicitly labels itself “Revised August 1, 2026”; all three foreign form instructions say “rev. 8/2026.” All responses were actual PDFs, not challenge pages.

| Initial foreign filing | Base state filing fee | Optional certified copy | Same-day surcharge | 24-hour / next-business-day surcharge |
| --- | ---: | ---: | ---: | ---: |
| Foreign corporation qualification | $245 | $50 | $100 | $50 |
| Foreign LLC certificate of registration | $200 | $50 | $100 | $50 |
| Foreign LP registration | $200 | $50 | $100 | $50 |

The fee schedule's foreign corporation “Qualification” row (page 2) reads `$245.00 / $50.00 / $100.00 / $50.00` under state filing, certified copy, same day, and 24-hour columns. The foreign LLC certificate row and domestic/foreign LP filing row (page 3) specify `$200.00 / $50.00 / $100.00 / $50.00`. The corporation form independently states: “The fee to file the Qualification Certificate is $245.” LLC/LP instructions likewise state $200. Agent designation is part of the filing form; no separate initial agent-designation government surcharge is listed in these rows. A private agent's service price remains additional and is not fixed by these fees.

The current form instructions confirm six-month existence evidence and a complete Delaware street address for the agent. They require a specific business purpose, not a general-purpose statement. Corporate execution must be by an authorized officer; LLC execution by an authorized person; LP execution by a general partner and names/addresses of all general partners must be provided. The corporation cover instructions confirm the first $250 annual report is due June 30 of the year following the calendar year in which qualification becomes effective. LLC/LP instructions confirm first $400 annual tax is due June 1 following the close of the registration calendar year.

The actual [SOS expedited guidance](https://corp.delaware.gov/expserv/) was reviewed:

| Service | Additional state fee | Stated processing / Eastern cutoff |
| --- | --- | --- |
| One hour | $1,000 | Within one hour of receipt; received by 21:00 |
| Two hour | $500 | Within two hours; received by 19:00 |
| Same day initial foreign filing | $100 for each of the three types | Received before 14:00 |
| Next business day initial foreign filing | $50 for each of the three types | Next business day, excluding holidays/weekends; received by 19:00 |

These are additional government fees, not private agent service pricing. The specific same-day and 24-hour amounts above come from the reviewed August 2026 schedule; the general expedited webpage covers a wider range of filings and quotes $100–$200 / $50–$100 ranges. The schedule says one/two-hour fees apply “per document/request” and that same-day/24-hour fees apply “per file number.” The SOS cautions that processing varies with volume and filing errors. Return delivery is normally routine postal service unless FedEx/UPS account information is supplied; mail time is additional and results are not returned by email or fax. No fixed normal-processing guarantee was inferred. The $200 statutory / $250 SOS annual late-penalty conflict remains unresolved; the fee schedule concerns filing/copy services and does not reconcile that late charge.

## Reviewed-source retrieval evidence

Hashes refer to full original response bytes, including PDF bytes before text extraction. HTML site navigation is included in the HTML digest. `Mozilla/5.0` was used for official statutory sources after the source's Azure gateway rejected the default agent; ordinary proxied HTTPS and TLS verification remained enabled. A 244-byte “Request Rejected” response from a different agent setting was discarded and never counted as verified content.

| Reviewed official source | Retrieved at (UTC) | SHA-256 of retrieved bytes |
| --- | --- | --- |
| [de_title8](https://delcode.delaware.gov/title8/title8.pdf) | 2026-10-10T04:22:01.558018+00:00 | `1ed2c5bafb169b1df54d91972253405126e1403087ff7262fc2549aa72228b3e` |
| [de_title6](https://delcode.delaware.gov/title6/title6.pdf) | 2026-10-10T04:22:01.559068+00:00 | `fed9089f9b3ab30fe6fae338deb2280dc1a4cdb523c985de551f3171247c1e19` |
| [de_corp_foreign_code](https://delcode.delaware.gov/title8/c001/sc16/index.html) | 2026-10-10T04:22:01.973858+00:00 | `28fc171719187139cde83ba0ca6b8661cca3d2aeb6b11d3b0ff1a171500b9f5f` |
| [de_corp_fees_code](https://delcode.delaware.gov/title8/c001/sc18/index.html) | 2026-10-10T04:22:37.411906+00:00 | `5a59b87609ce381d0fed9d2fa157195bd5ecb302b69f62d91a6378a20cb5a7e6` |
| [de_llc_code](https://delcode.delaware.gov/title6/c018/sc09/index.html) | 2026-10-10T04:22:01.763125+00:00 | `63828cb7e882bda900121b0f957ddc810988456925daf45992e06f91c3fbd2dc` |
| [de_lp_code](https://delcode.delaware.gov/title6/c017/sc09/index.html) | 2026-10-10T04:21:04.490484+00:00 | `fe2e00a9531df9b33b169d69a0bace872bada0535b4cb37644d69f439fce6c7a` |
| [de_tax_llc_code](https://delcode.delaware.gov/title6/c018/sc11/index.html) | 2026-10-10T04:22:01.843102+00:00 | `fe394ea173e7904410b1ccbb80213561cd958e38e31c2f15c9da42d874342ecd` |
| [de_tax_lp_code](https://delcode.delaware.gov/title6/c017/sc11/index.html) | 2026-10-10T04:22:01.877356+00:00 | `a197a690cfd12cf88b979a15568f043e974ea4fd745fda14fbc6d5beef1eb8aa` |
| [de_taxes](https://corp.delaware.gov/alt-entitytaxinstructions/) | 2026-10-10T04:21:03.070058+00:00 | `e6ce182e21bc251a49c42e82c9f9bafccfbb2e28f7d655cfc4963bb42f874c60` |
| [de_paytax](https://corp.delaware.gov/paytaxes/) | 2026-10-10T04:21:03.819023+00:00 | `d59422eff8e1b03aa238390520f2fa93f82851b3eec4f8e5090e55f06f646169` |
| [de_expedite](https://corp.delaware.gov/expserv/) | 2026-10-10T04:21:03.863736+00:00 | `440d7ab7848e52d55f7264b5db63827d1b2bbe93b411334c3b6a8a0a2c840926` |
| [de_fee](https://corp.delaware.gov/fee/) | 2026-10-10T04:22:37.410800+00:00 | `b34925ff7aa5977d7e8ec2b0c3201ca64c63334858c9f1289492170d39461ffb` |
| [de_forms](https://corp.delaware.gov/corpforms/) | 2026-10-10T04:22:37.410227+00:00 | `47a415a2f64b277265ac2a258a4c45f56a0dbe540dc9b8fb70754e2ec532e3d6` |
| [de_corp_forms](https://corp.delaware.gov/corpformsforcorp09/) | 2026-10-10T04:24:37.926907+00:00 | `d5287b2a0a9b669737127c3da42ff38b57cb927d4f54f32cda9126deea55eece` |
| [de_llc_forms](https://corp.delaware.gov/corpformsllc09/) | 2026-10-10T04:24:37.927934+00:00 | `b3b77a8e6a29e28387e63b0182fcdc60f3c204fda77f330598a3db041e844106` |
| [de_lp_forms](https://corp.delaware.gov/corpformslp09/) | 2026-10-10T04:24:37.928577+00:00 | `653468a6e14c52d9b32983c4f606a58f0fdec2ec9676b48b33fc6f645a19771c` |
| [de_fee_pdf](https://corpfiles.delaware.gov/Fee_Schedule/AugustFee2026.pdf) | 2026-10-10T05:47:04.770410+00:00 | `129f34df2adcf5f88136a54dad1a3a053f415d2d1a0d416f0df1c9eec7a0aacc` |
| [de_corp_form_pdf](https://corpfiles.delaware.gov/Foreign_Corp/Foreign%20Corporation.pdf) | 2026-10-10T05:47:04.770925+00:00 | `fea4e5be3e3684cbfde4f9794896b74083e6941942f35ac924e1659fdeb06d59` |
| [de_llc_form_pdf](https://corpfiles.delaware.gov/LLC_Forms/Foreign%20LLC.pdf) | 2026-10-10T05:47:04.771281+00:00 | `cefbb73eb084979ba3101b79c31960919b126507535907d652313594499de0ba` |
| [de_lp_form_pdf](https://corpfiles.delaware.gov/LP_Forms/Foreign%20LP.pdf) | 2026-10-10T05:47:04.771595+00:00 | `c0c45833a7f9868320607ade13783d7f31f95c96cab62ebb7ec6e20d379390f3` |
