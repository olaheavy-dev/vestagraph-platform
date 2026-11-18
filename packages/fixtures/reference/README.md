# Reference data

Real official data, unlike the invented files in `data/`. Each table lives in one JSON file checked by the schema of the same name in `../schema/` (`make validate`), and names its source URL and effective date (AGENTS.md rule 3). These are words for codes, not tax, legal, tenancy or privacy rules.

## `energy-code-tables.json` (DA-09, energy certificate by certificate number)

Words for the codes in an energy certificate record: `propertyType`, `builtForm` and `improvement` (the register's `improvement_number`). **Partial** (`"partial": true`): until the build stage it holds only the codes the sample certificates in `data/energy-certificates.json` use; the full tables for every schema in scope come with the page's build. A code with no entry must show "Not on this certificate", never the raw code (design 2026-11-18).

| Table | Source | Effective date |
|---|---|---|
| `propertyType`, `builtForm` | `PropertyTypeCode` and `SAP-BuiltFormCode` in `SAP-Domains.xsd` of RdSAP-Schema-21.0.1, in the energy certificate register's published schemas (MHCLG `epb-data-warehouse` repository, pinned to commit `d7adc11`) | as published (the file states none); checked 18 Nov 2026 |
| `improvement` | the England and Wales (`EAW`) block of `ExternalDefinitions.xml` of RdSAP-Schema-21.0.1, `Improvement-Summary` (language 1, English), same repository and commit | revision 8.1, dated 3 Jun 2025; checked 18 Nov 2026 |

- Words are copied as published, except that a non-breaking space is written as an ordinary space.
- Code meanings can vary between schema versions ([codes API documentation](https://get-energy-performance-data.communities.gov.uk/api-technical-documentation/codes-info)); these tables come from RdSAP 21.0.1 only. The sample certificate on an older SAP schema (G) therefore holds no property type or built form code.
- The register's own codes endpoint needs a bearer token, so the tables come from the published schema files, which are the register's definitions of these codes. Licence: Open Government Licence v3.0, as for the register's open data.
