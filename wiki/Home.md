# SHAP Driven Adverse Action

This wiki walks through work I did at Varo on the adverse action side of two lending products, VA Day Zero and VA Classic.

The short version: when the model declined someone or cut their line, the system used SHAP to explain why, and turned that explanation into the reason codes on the customer letter. The idea was sound going in. The way it got implemented had a few real problems, and fixing those problems is most of what this repo covers.

All figures here (the validation match rate, the lookback windows, the reason code list) come from the actual work. No real customer data, model artifact, or coworker name appears anywhere in this repo. People are described by role, not by name.

Pages:

- [The problem](Problem.md)
- [Stakeholders](Stakeholders.md)
- [The fix](The-Fix.md)
- [Validation and outcomes](Validation-and-Outcomes.md)
- [Lessons](Lessons.md)

For the actual code, see the [repo root](https://github.com/ali8gates/shap-adverse-action).
