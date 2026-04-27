# The Goals We Were Optimizing For

Scoring the applicant was never the hard part. The hard part was explaining a decline or a line cut in a way that actually held up: matched what the model did for that specific person, and would still hold up if someone in model risk or compliance pulled it apart line by line.

I framed the work around three goals.

## Explainability that matches what actually happened

Every reason on a letter needed to be a true reflection of that applicant's own SHAP values, not a proxy or a rule of thumb that usually holds. That is what drove the fix to per-record SHAP direction and to selecting reasons by sign instead of by size.

## Something second line and compliance could actually audit

Second line model risk and compliance needed to walk any single file end to end: the data that went in, the features built from it, the model score, the SHAP based reasons, and the letter that went out. The goal was zero cases where the reasons on a letter did not line up with the underlying feature values or the model's own risk logic.

## Room to price and decline based on real risk

None of the rest mattered if it did not change how the business could act. Before this, a real decline the team could not fully defend often became a small line instead. Getting the explanation right gave risk and credit policy a reason they could stand behind to actually decline or cut a line where the risk was real, instead of defaulting to something softer to avoid a reason code that would not survive scrutiny.

## What we measured against each goal

**Fidelity.** Shadow scoring and historical backfills, including the March 31 validation slice, compared feature values, model scores, and the reasons a letter would carry against what was already live. On that slice, all three lined up completely: no training serving skew, and no missing or mismatched reason codes. The two bugs that used to cause a mismatch, batch mean direction and magnitude based selection, were the two we fixed first, because everything downstream depended on getting those right.

**Operational reliability.** Earlier versions of the pipeline had reason codes with no matching template text, which produced blank or partial letters, multi-reason decisions that only rendered the first reason, and no defined path for applicants with no usable data at all. All three gaps got closed. Every code now has approved text or the letter fails before it goes out, rendering always walks the full reason list, and a fully null feature set gets an explicit insufficient information response instead of silently falling through.

**Governance and decisioning.** Second line model risk reviewed the SHAP distributions, monotonicity, and reason hierarchy for both products, and compliance reviewed example letters directly, before any of this reached a real customer. That review is what let the business actually rely on it. A decline or a line cut backed by a reason that traces back to that applicant's own data is something product, data science, and compliance could all stand behind, not just something that looked reasonable on paper.
