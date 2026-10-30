# Domestic US company formation guides — research track

This is separate from the site's existing **foreign qualification** content.
A new company formed in its home state is not registering an existing foreign entity.

## Research deliverable

`python -m us_new_entities.formation_guides formation-drafts` creates 100
**unverified, noindex** research drafts: one LLC and one corporation for each
of the 50 states. The District of Columbia is intentionally excluded.

These drafts must **not** be copied into the production deployment or
submitted as finished state guides.

Each record requires individually verified official evidence for:

1. Domestic formation form, with direct filing URL.
2. State filing fee and any legally required additional charges.
3. Registered-agent eligibility and address requirements.
4. Business name selection and availability.
5. Online/mail/in-person filing options and restrictions.
6. Initial reports, publication, or organizational notices.
7. Recurring reports, franchise taxes, and state taxes, separately identified.
8. State-specific exceptions, industry/professional licensing, and eligibility.

Store source URL, exact claim, retrieval date, reviewed date, effective date
when available, and unresolved conflicts. Never infer an omitted state
requirement from the existing FOREIGN qualification registry.

Publication gate: require all mandatory fields verified with government sources
and explicit reviewer approval before indexable HTML, schema offers,
sitemap inclusion or Northwest affiliate calls-to-action are added.
Fees or links that cannot be verified must not be invented.

Three initial official entrypoints exist for CA, DE and TX; an entrypoint
alone does not establish review of the mandatory fields.

**Progress:** Research scaffolding built; 0/100 formation guides
independently verified or approved for publication in this branch.
