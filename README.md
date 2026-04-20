# SHAP Driven Adverse Action

A walkthrough of work I did at Varo fixing the adverse action explanations behind two lending products, VA Day Zero and VA Classic. When the model declined an applicant or cut their line, the system used SHAP to explain why and turned that explanation into the reason codes on the customer letter. The idea was right. The implementation had real problems, and fixing them is most of what this repo covers.

Before this fix, a real denial the team could not fully defend often became a small dollar line instead, something like $20, rather than an actual decline. That protected against a bad reason showing up on a letter, but it also meant known risk stayed on the book and pricing never reflected it. After this fix, a decline or a line cut comes with reasons that trace back to that specific applicant's own data, checked before they ever reach a letter.

Everything in this repo uses synthetic, invented data. Real customer records, real model output, and real coworker names never appear here. The numbers I do use, the validation match rate, the lookback windows, the reason code catalog, come from the actual work.

## What's here

- [The problem](wiki/Problem.md), what the adverse action pipeline actually looked like and where it broke
- [Stakeholders](wiki/Stakeholders.md), who was in the room and how the work got split
- [The fix](wiki/The-Fix.md), the direction bug, the selection bug, and the data and pipeline hardening that went with them
- [Validation and outcomes](wiki/Validation-and-Outcomes.md), how this got proven out before it shipped, and what changed
- [Lessons](wiki/Lessons.md), what generalizes past this one pipeline
- [The code](src/shap_aa/), a runnable version of the fixed logic, synthetic data only

## Run the demo

```
cd src
python -m shap_aa.cli
```

This runs five synthetic sample applicants through the full decision pipeline (a clean decline, a line decrease, a clean approval, an insufficient information case, and a case held for review over a data contract mismatch), prints each decision with its reason codes, and then walks through a shadow scoring and backfill comparison. Nothing here reaches a real system, everything is invented data checked into this repo.

Run the tests with:

```
python -m pytest tests
```

26 tests cover the direction logic, the reason selection logic, the data contract checks, the template quality gate, the full pipeline, and the backfill comparison.

## The whiteboards

The three boards under [excalidraw/](excalidraw/) were built as real Excalidraw scenes:

- `board-1-the-problem.excalidraw`, the pipeline before this fix and where each piece of it broke
- `board-2-the-fix.excalidraw`, the direction, selection, data, and pipeline fixes side by side
- `board-3-validation-and-outcomes.excalidraw`, how it was validated and what changed as a result

Each `.excalidraw` file opens directly in [Excalidraw](https://excalidraw.com), drag it onto the canvas or use File, Open. The matching `.png` next to each one is a static preview so the boards show up on GitHub without opening the app.

## A note on scope

This repo covers the SHAP explainability layer and the adverse action pipeline built on top of it, not the underlying credit model itself. Any figures I mention (the validation match rate, the lookback windows) describe this pipeline, not the underlying model's performance or the credit decision process more broadly.
