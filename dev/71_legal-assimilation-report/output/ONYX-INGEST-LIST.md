# Onyx ingest list — legal "gold" pass

Onyx @ `http://localhost:3000` had **0 connectors / 0 documents** on 2026-09-19. The report was written without retrieval. To turn it into a source-grounded comparison, add a **Web connector** (or "Web crawl" set to single pages) for each URL below, then ask Onyx the §-questions from the report with citations on.

Primary law first; guidance second; vendor terms third. UK-only. Nothing here is a login or a secret.

## A. Primary legislation (legislation.gov.uk — current version)
- https://www.legislation.gov.uk/ukpga/2005/5/part/6A — ITTOIA 2005 Pt 6A trading allowance
- https://www.legislation.gov.uk/ukpga/2006/46/part/41 — Companies Act 2006 Pt 41 business names
- https://www.legislation.gov.uk/uksi/2013/3134/contents — Consumer Contracts Regs 2013
- https://www.legislation.gov.uk/ukpga/2015/15/contents — Consumer Rights Act 2015
- https://www.legislation.gov.uk/ukpga/2024/13/part/4 — DMCC Act 2024 Pt 4 unfair commercial practices
- https://www.legislation.gov.uk/ukpga/2000/8/section/19 — FSMA s.19
- https://www.legislation.gov.uk/ukpga/2000/8/section/21 — FSMA s.21
- https://www.legislation.gov.uk/uksi/2001/544/contents — Regulated Activities Order 2001 (arts 25, 53)
- https://www.legislation.gov.uk/ukpga/2005/19/section/3 — Gambling Act 2005 s.3
- https://www.legislation.gov.uk/eur/2016/679/contents — UK GDPR (retained)
- https://www.legislation.gov.uk/ukpga/2018/12/contents — Data Protection Act 2018
- https://www.legislation.gov.uk/uksi/2018/480/contents — DP (Charges and Information) Regs 2018
- https://www.legislation.gov.uk/uksi/2003/2426/regulation/22 — PECR reg.22
- https://www.legislation.gov.uk/ukpga/1988/48/section/11 — CDPA s.11 (also s.9, s.90)
- https://www.legislation.gov.uk/ukpga/1990/18/contents — Computer Misuse Act 1990
- https://www.legislation.gov.uk/ukpga/2006/35/section/2 — Fraud Act 2006 s.2
- https://www.legislation.gov.uk/uksi/2002/2013/regulation/6 — E-Commerce Regs reg.6

## B. Regulator guidance
- https://www.gov.uk/guidance/tax-free-allowances-on-property-and-trading-income
- https://www.gov.uk/register-for-self-assessment
- https://www.gov.uk/self-employed-national-insurance-rates
- https://www.gov.uk/simpler-income-tax-cash-basis
- https://www.gov.uk/self-employment-and-universal-credit
- https://ico.org.uk/for-organisations/data-protection-fee/self-assessment/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/uk-us-data-bridge/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/
- https://www.handbook.fca.org.uk/handbook/PERG/2/ — FCA PERG 2 (authorisation)
- https://www.handbook.fca.org.uk/handbook/PERG/8/ — FCA PERG 8 (financial promotion)
- https://www.gov.uk/government/publications/unfair-commercial-practices-cma207 — CMA DMCC guidance
- https://www.asa.org.uk/codes-and-rulings/advertising-codes/non-broadcast-code.html — CAP Code
- https://www.gov.uk/government/publications/business-names-guidance — Companies House business names

## C. Vendor terms (processor / transfer evidence)
- https://render.com/dpa — Render Data Processing Addendum
- https://render.com/docs/regions — Render regions
- https://openrouter.ai/privacy — OpenRouter privacy
- https://openrouter.ai/terms — OpenRouter terms

## D. Repo docs to index alongside (local file connector, read-only)
- `mechanicall-os/CURRENT.md`, `SPEC-v0.2.md`, `PRODUCT.md`, `CORE_PRINCIPLES.md`
- `mechanicall-os/templates/alias/*.md`
- `~/sites/anphuni.com-repo/public/privacy.html`, `contact.html`
- `dev/71_legal-assimilation-report/output/LEGAL-ASSIMILATION-REPORT.md` (so Onyx can be asked to challenge it)

## Questions to put to Onyx once indexed
1. For each §1–§11 claim marked "verify", quote the section that supports or contradicts it.
2. Is holding a client's project material within the ICO fee exemption for "accounts and records"? Cite.
3. Does a random-walk paper trader using real ticker names fall within RAO art 53 or FSMA s.21? Cite PERG.
4. What must appear on a sole trader's website under CA 2006 s.1202 and ECR reg.6? List verbatim.
5. Current-year figures: trading allowance, Class 2/4 thresholds, CGT AEA, ICO tier-1 fee.
