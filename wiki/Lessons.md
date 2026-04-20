# Lessons

A few things that generalize past this one pipeline.

**Using SHAP is not the same as using it correctly.** SHAP gives you a number and a sign for every feature and every record. What actually determines whether that becomes a defensible reason is how you turn it into something per-customer, directional, and limited to the reasons that actually increased risk. Skip any one of those and the explanation stops matching the decision.

**Adverse action is a pipeline problem, not a model problem.** The model can be scoring correctly and the explanation can still be wrong, because the bug sits in how the explanation gets computed and rendered, not in the score itself. Fixing this took changes in the SHAP direction logic, the reason selection logic, the data feeding the model, and the template rendering downstream of all of it.

**CRA and non-CRA alignment is not optional.** Two feeds that categorize the same transaction differently, or that pull different lookback windows, will quietly produce different features for what should be the same customer. That difference does not announce itself, it just shows up as a wrong reason code on a letter months later.

**Shadow mode and backfills are how you actually know it is fixed.** A fix that only exists in a code review or a unit test has not been tested against the thing that matters, real historical decisions. Running the new logic against real cohorts and comparing every value it touches is what turned "I think this is right" into "here is the match rate."

**Product and data science have to own this together.** Explainability lives at the boundary between what the model computed and what a customer or a regulator can actually understand. Neither side alone is positioned to catch every failure mode here, the direction bug and the selection bug both needed someone thinking about both the math and the customer experience at the same time.
