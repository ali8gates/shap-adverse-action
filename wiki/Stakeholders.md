# Stakeholders

Real names never appear in this repo. People here are described by role.

## Who was in the room

- Data science, who owned the model and the SHAP computation itself
- Product, who owned the policy layer, the reason code catalog, and how the customer letter reads
- Engineering, who owned the pipeline that ties scoring, explainability, and the letter together
- Second line model risk, who reviewed the SHAP distributions, monotonicity, and reason hierarchy before anything shipped
- Compliance, who reviewed the letter templates and the FCRA reasoning directly, and signed off before the fix went live

## How I worked with them

This was not a case of data science handing off a model and walking away. Getting adverse action right meant product and data science sitting together on what "risk increasing" actually means for a specific customer, and it meant engineering, model risk, and compliance all looking at the same backfill output before anyone was comfortable calling it fixed.

I owned the product side of this end to end: defining what a defensible reason code catalog looks like, working through the direction and selection bugs with data science until the logic matched how a person would actually read their own SHAP values, and running the validation process that model risk and compliance needed to sign off.

## Where this connects to the bigger picture

VA Day Zero and VA Classic are two different lending products with different underwriting models, but they share the same adverse action pipeline. Fixing the SHAP direction and selection logic, and hardening the CRA data contracts, benefited both products at once. The same validation approach, shadow scoring plus historical backfill plus dual review, is the pattern I would reuse for any future credit or risk model that needs a defensible customer facing explanation.
