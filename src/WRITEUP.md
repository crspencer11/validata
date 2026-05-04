# Validata — Take-Home Submission Writeup

---

## The Problem & Why I Chose It

During my time working with time-series data, I saw the pain of dealing with messy financial datasets as real and recurring. Before any analysis or modeling can happen, you typically have to manually audit for price spikes caused by bad ticks, timestamps that are duplicated or out of order from feed issues, and statistical outliers that skew everything downstream. Most of the time this is done ad hoc via a few pandas one-liners taped together, rewritten slightly differently each time. I wanted to build something I'd actually reach for: a small, opinionated CLI that handles the validation pass and gives you a repair option so you don't have to stare at a violations list and manually fix JSON.

The scope fit the assignment well too. Rule-based validation is naturally extensible and adding a new rule is but a few lines. With just a few rules you can still ship something useful. Also, working on related projects on the side, including a web scrapper + inference model for underlying assets.

---

## How I Used AI

I used Generative AI tools throughout. My workflow mostly followed writing a rough intent in a comment or a short description of what I wanted with a basic code implementation/example. I then let it scaffold the rest of the structure, then read and refactor what ws returned.

It was most useful for the boilerplate-heavy parts: setting up the Click CLI with the right option types, wiring together the `ValidationResult` dataclass, and writing the initial rule abstractions. That saved probably an hour of setup I'd otherwise just copy from a previous project.

For the statistical outlier rule I asked it to implement z-score detection, and it did so correctly on the first pass. That one I kept almost verbatim.

I used it less for the repair logic. I had a specific opinion about how I wanted repairs to live alongside rules rather than in a separate repair class, so I wrote most of that by hand. I also consciously decided against reaching for Pydantic for the data models. It's genuinely useful when you're parsing external untrusted input, but `Violation` and `ValidationResult` are only ever constructed internally by code I control. Dataclasses are the right tool here. Adding Pydantic would've been over-engineering for the sake of it.

---

## Where the AI Got Things Wrong

The biggest concrete issue: the tests AI tooling generated didn't match the actual interfaces it had written a few turns earlier. The `test_engine.py` tests were asserting dict access — `result["status"]`, `result["count"]` — but the engine returns a `ValidationResult` dataclass with attribute access. Those tests fail immediately on run.

The repair tests were worse, and honestly this is the jankiest part of the submission. They import `from src.repair import Repairer`, but the class in `repair.py` is `DataRepairer`, and it exposes none of the methods the tests expect. Claude had quietly generated two parallel repair implementations in the same session. One embedded in the rules (which the engine actually calls), and a standalone `DataRepairer` class that nothing ever imports. The tests were written against the dead one. I didn't catch it until I ran the suite and everything errored.

I fixed the engine and rules tests, rewrote the repair tests to target the rule-based repair that's actually implemented, and cleaned up a few other things. Notice when violations exceed the 20-row table limit, and a guard against empty input in `StatisticalOutlierRule` that would otherwise crash with a `ZeroDivisionError`. None of those were hard fixes, but they took time I hadn't budgeted.

---

## What I'd Improve with More Time

**Better repair strategies.** The price spike repair just averages the spike with its neighbor, which is a pretty naive approach. A real tool would want at least a few strategies per rule, such as carry-forward, rolling median, drop-and-interpolate, and a way to choose between them.

**CSV support.** The tool only accepts JSON right now. Most raw financial data lives in CSV. This would probably be the highest-value addition for real-world use.

**YAML rule config.** Threshold and z-score parameters are currently CLI flags. If you're validating many datasets with different tolerances, you'd want a config file. That is when I'd consider leveraging Pydantic. For parsing external user-defined config with real validation and helpful error messages.

**Richer repair output.** Right now repair just returns the corrected dataset. More useful would be a diff to see what changed, why, and which rule caused it, so you can review before committing.

---

## Limitations & Rough Edges

- The statistical outlier rule computes z-scores against the full dataset with no windowing. For long time series with regime changes(i.e a price that legitimately doubles over six months) it will flag real data as anomalies. It's fine for short, stable series and actively wrong for anything else.
- Repair is destructive and unaudited. There's no dry-run, no confirmation prompt, no log of what changed. For anything beyond a quick scrub of toy data, that's a real problem.