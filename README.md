# Agentics Challenges

This repository hosts public challenge proposals for Agentics. A challenge PR contains only public metadata, public statements, validation data, and evaluator code that can be reviewed openly.

Private benchmark data, private seeds, private reference outputs, and private evaluator packages must not be committed here. Upload those assets directly to Agentics as private asset ZIP overlays for the draft.

## Add a Challenge

1. Fork this repository and create `challenges/<challenge-name>/`.
2. Add `agentics.challenge.json` at the challenge root.
3. Add a versioned bundle, usually `v1/`, with `spec.json`, `statement.md`, public validation data, and evaluator code.
4. Declare any required private assets in `agentics.challenge.json`.
5. Open a pull request against this repository.
6. Sign in to the Agentics creator console at `/creator` with GitHub OAuth, create a draft from the reviewed PR metadata, and upload any private asset ZIP overlays there.

The public challenge_name must be reviewed before publish. Use lowercase ASCII letters, digits, and single hyphens, and keep the directory name equal to the id.

## Private Assets

Private assets are ZIP overlays extracted onto the runtime bundle only during Agentics admin validation and publishing. Common asset kinds are:

- `private_benchmark_data`: static official benchmark files.
- `private_seeds`: private seed or config files used by a prepare phase.
- `private_reference_outputs`: private expected outputs.
- `private_evaluator_package`: private evaluator code or resources.

For generated official data, prefer a small `private_seeds` overlay plus an evaluator-owned prepare phase. The challenge owner is responsible for reproducibility and reliability of generated or externally downloaded data.

Creator-side draft creation and private asset upload are web-only for the MVP. The Agentics CLI only provides admin reviewer helpers until it supports GitHub OAuth creator sessions.

## Local Validation

Run:

```sh
python3 scripts/validate_challenges.py
```

This CI check verifies public manifests, public validation run manifests, public `source_path` files, and obvious private-data leaks. Agentics server-side validation remains the authoritative publish gate.
