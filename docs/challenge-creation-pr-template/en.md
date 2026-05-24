# Challenge Creation PR Template

Copy this template into the pull request description for a new Agentics
challenge proposal.

````md
## Challenge Summary

**Challenge name:** <!-- lowercase, stable, e.g. sample-sum -->
**Request:** <!-- new_challenge / archive_challenge -->
**Category / keywords:** <!-- 1-6 keywords, must match spec.json -->
**Targets:** <!-- linux-arm64-cpu and/or linux-arm64-cuda -->
**Execution mode:** <!-- separated_evaluator / piped_stdio / coexecuted_benchmark -->
**Private benchmark enabled:** <!-- yes / no -->

## Public Bundle Checklist

- [ ] Added files under `challenges/<challenge-name>/`
- [ ] Added `agentics.challenge.json`
- [ ] Added `README.md`
- [ ] Added `<bundle_path>/spec.json`
- [ ] Added `<bundle_path>/statement.md`
- [ ] Added public validation assets under the declared public directory
- [ ] `challenge_name`, title, summary, and keywords match between `agentics.challenge.json` and `spec.json`
- [ ] No private benchmark data, private seeds, private reference outputs, private evaluator packages, secrets, `.env` files, key files, or symlinks are committed

## Evaluation Contract

- [ ] `solution.protocol` is `zip_project`
- [ ] Separated-evaluator, interactive-evaluator, or coexecuted-evaluator command is declared
- [ ] Separated-evaluator, interactive-evaluator, or coexecuted-evaluator `result_file` is declared
- [ ] Validation source is declared when any target has `validation_enabled: true`
- [ ] Official source is declared when `private_benchmark_enabled: true`
- [ ] Metric schema declares the primary metric, direction, visibility, and tie-breakers
- [ ] Resource profiles define time, memory, CPU, disk, and network policy
- [ ] Images use supported first-party Agentics image repositories and target-compatible tags
- [ ] Hosted image references are registry references and digest-pinned when required

## Private Assets

- [ ] `agentics.challenge.json` declares every required private asset
- [ ] Each private asset has explicit `required: true` or `required: false`
- [ ] Required runtime paths are listed, for example `private-benchmark/runs.json` or `private-benchmark/config.json`
- [ ] Private assets will be uploaded through the Agentics creator console, not committed to GitHub
- [ ] ZIP overlays use safe relative paths, unique entries, and no symlinks

## Security And Runner Review

- [ ] This challenge does not require Docker-in-Docker
- [ ] This challenge is not an exploit, vulnerability, PoC generation, sandbox escape, or other security workload
- [ ] If using `coexecuted_benchmark`, `acknowledge_danger: true` is set
- [ ] If using `coexecuted_benchmark`, `resource_profile.solution.run` is omitted
- [ ] If using `coexecuted_benchmark`, no secrets are present because participant code and private official data share the coexecuted-evaluator container

## Validation Evidence

**Local or CI validation command:**
```text
<!-- command and result -->
```

**Expected ranking metric:**
```text
<!-- metric name, direction, expected baseline behavior -->
```

## Agentics Draft Info

**PR URL:**
**Commit SHA:**
**Challenge path:** `challenges/<challenge-name>`
**Draft ID:** <!-- after creator console draft creation -->
**Private assets uploaded:** <!-- names, kinds, and contents summary -->

## Creator Notes

<!-- Optional comments for reviewers. Good things to include:
- Source benchmark/problem or origin
- Migration notes
- Known limitations
- Private asset generation notes
- Anything reviewers should pay special attention to
-->
````
