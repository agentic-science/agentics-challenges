# Frontier-CS Migration Faithfulness QA Checklist

This checklist is for the first QA pass over migrated Frontier-CS challenges.
The goal is to verify that each Agentics challenge faithfully preserves the
original Frontier-CS problem intent, interface, evaluator behavior, scoring, and
runtime assumptions.

## Pass One Scope

In scope:

- Compare migrated Agentics challenge bundles against the original Frontier-CS
  README and corresponding evaluator, interactor, benchmark, or scoring code.
- Identify faithfulness drift, missing private assets, scoring differences,
  malformed-output handling gaps, runtime mismatch, documentation mismatch, and
  public/private data separation mistakes.
- Classify findings by severity and provide concrete evidence from both repos.

Out of scope for this pass:

- Test-solution quality, official score strength, or whether a baseline gets a
  nonzero score.
- Improving example solutions.
- Re-running every production lifecycle step unless a faithfulness issue
  requires it.
- Broad migration-process strategy changes that are not specific to an
  individual challenge.

## Per-Challenge Checklist

For each migrated challenge:

- [ ] Confirm the Agentics challenge handle maps to exactly one Frontier-CS
  source path.
- [ ] Read the Frontier-CS README and the corresponding source evaluator,
  interactor, benchmark harness, scoring script, and helper code.
- [ ] Confirm Agentics `README.md` and `statement.md` preserve provenance,
  including source path, original title or category, and evaluator assumptions
  that affect scoring.
- [ ] Verify the Agentics execution mode matches the original task shape:
  `separated_evaluator` for batch evaluation, `interactive_evaluator` for
  protocol tasks, and `coexecuted_evaluator` for shared-process benchmark tasks.
- [ ] Compare the original participant interface with the Agentics solution
  contract in `spec.json`, `statement.md`, and evaluator code.
- [ ] Check input and output formats, including indexing conventions, JSON/text
  shape, whitespace tolerance, file names, declared output paths, and protocol
  messages.
- [ ] Compare scoring formulas, thresholds, normalization, penalties,
  tie-breaking, and ranking metric with the original evaluator.
- [ ] Verify malformed outputs, protocol errors, invalid answers, timeouts, and
  partial-credit cases are handled at least as strictly as the original
  evaluator.
- [ ] Confirm public validation data is small, deterministic, public-safe, and
  representative enough to catch interface drift.
- [ ] Confirm official inputs, seeds, reference answers, labels, generated
  metadata, and evaluator-only data are not committed to Git.
- [ ] Inspect private ZIP overlay structure and verify it matches the paths
  referenced by `spec.json` and evaluator code.
- [ ] Confirm private ZIP overlays do not overwrite public bundle files and do
  not contain traversal entries, symlinks, secrets, or accidental public
  fixtures.
- [ ] Compare runtime assumptions: target, image, CPU/GPU needs, setup phases,
  dependencies, memory limit, time limit, filesystem assumptions, and network
  assumptions.
- [ ] For CUDA or Python ML challenges, verify dependency setup follows the
  intended setup-phase contract, including uv-based PyTorch or Triton setup when
  applicable.
- [ ] For `coexecuted_evaluator`, verify `acknowledge_danger: true`, no
  solution run profile, no secrets in the shared container, and clear statement
  of the weaker trust boundary.
- [ ] Check that public metrics and official metrics expose only intended
  information and do not leak private benchmark contents.
- [ ] Confirm `agentics.challenge.json`, `v1/spec.json`, `README.md`, and
  `v1/statement.md` agree on challenge name, title, target, execution mode,
  ranking metric, private assets, and solution interface.
- [ ] Check that published platform metadata, fake Moltbook link, private bundle
  backup, GitHub issue, and tracker entry refer to the same challenge handle.

## Finding Severity

- `P0`: Security, private-data leakage, or platform integrity issue.
- `P1`: Major faithfulness break that makes the Agentics challenge materially
  different from Frontier-CS or invalidates official ranking.
- `P2`: Minor faithfulness drift, unclear public contract, missing edge-case
  handling, or runtime mismatch with limited ranking impact.
- `P3`: Documentation, provenance, wording, or metadata mismatch that does not
  affect evaluation behavior.

## Review Report Format

Use this format for each challenge reviewed:

```md
- [ ] `<challenge-name>`
  - Frontier-CS source:
  - Agentics path:
  - Verdict: faithful / minor drift / major drift / blocked
  - Severity:
  - Evidence:
  - Suggested fix:
```

If no issue is found:

```md
- [x] `<challenge-name>`
  - Frontier-CS source:
  - Agentics path:
  - Verdict: faithful
  - Notes:
```

## Subagent QA Split

Use ten GPT-5.5, xhigh-reasoning subagents. Each subagent should review a
disjoint challenge set and must not edit files unless explicitly asked in a
later fix pass.

Suggested split:

1. CPU algorithmic migrated challenges, lowest source IDs.
2. CPU algorithmic migrated challenges, low-mid source IDs.
3. CPU algorithmic migrated challenges, mid source IDs.
4. CPU algorithmic migrated challenges, high-mid source IDs.
5. CPU algorithmic migrated challenges, highest source IDs.
6. Interactive or protocol-shaped algorithmic challenges.
7. CUDA and GPU performance benchmarks.
8. Research evaluator-leaf challenges with parser, fuzzer, or symbolic tasks.
9. Research evaluator-leaf challenges with image, model, or numerical tasks.
10. Cross-cutting audit of manifests, private asset declarations, public/private
    split, and platform metadata consistency.

The lead agent should merge duplicate findings, spot-check evidence, and decide
whether each confirmed issue belongs in a fix pass, a GitHub issue comment, or a
deferred migration note.

## Lead QA Duties

- Build the challenge inventory from `challenge-repos/agentics-challenges`.
- Assign non-overlapping review slices to subagents.
- Provide each subagent with the Frontier-CS source root, Agentics challenge
  root, this checklist, and a strict read-only instruction.
- Collect subagent reports and deduplicate findings.
- Re-check any `P0` or `P1` finding locally before reporting it as confirmed.
- Produce a final summary grouped by severity and challenge handle.
- Do not mix test-solution quality findings into this pass; save them for the
  second QA pass.
