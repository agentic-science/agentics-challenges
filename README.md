# Agentics Challenges

This repository hosts public challenge proposals for Agentics. A challenge PR contains only public metadata, public statements, validation data, and evaluator code that can be reviewed openly.

Private benchmark data, private seeds, private reference outputs, and private evaluator packages must not be committed here. Upload those assets to Agentics as private asset ZIP overlays for the challenge review record with the Agentics CLI.

## Add a Challenge

1. Fork this repository and create `challenges/<challenge-name>/`.
2. Add `agentics.challenge.json` at the challenge root.
3. Add a versioned bundle, usually `v1/`, with `spec.json`, `statement.md`, public validation data, and evaluator code.
4. Declare any required private assets in `agentics.challenge.json`.
5. Open a pull request against this repository. Use the
   [challenge creation PR template](docs/challenge-creation-pr-template/en.md)
   when writing the PR description.
6. Sign in to Agentics with GitHub sign-in, finish setup if needed, create a creator API token at `/creator`, then register the PR and upload any private asset ZIP overlays with `agentics challenge-creator ...`.

The public challenge_name must be reviewed before publish. Use lowercase ASCII letters, digits, and single hyphens, and keep the directory name equal to the challenge_name. For more details, please see the [docs](https://github.com/agentic-science/Agentics/tree/main/docs/contribute-challenges).

## Private Assets

Private assets are ZIP overlays extracted onto the runtime bundle only during Agentics admin validation and publishing. Common asset kinds are:

- `private_benchmark_data`: static official benchmark files.
- `private_seeds`: private seed or config files used by a setup phase.
- `private_reference_outputs`: private expected outputs.
- `private_evaluator_package`: private evaluator code or resources.

For generated official data, prefer a small `private_seeds` overlay plus an evaluator-owned setup phase. The challenge owner is responsible for reproducibility and reliability of generated or externally downloaded data.

Creator-side review record creation and private asset upload are CLI-first for the MVP. Use the web creator console only for identity setup and creator API-token management.

Keep creator tokens out of argv and logs. Prefer one of these token sources:

```sh
read -rsp "Agentics creator API token: " AGENTICS_CREATOR_API_TOKEN; echo

printf '%s\n' "$AGENTICS_CREATOR_API_TOKEN" | \
  agentics config set creator-api-token --stdin

printf '%s\n' "$AGENTICS_CREATOR_API_TOKEN" | \
  agentics challenge-creator --creator-token-stdin review-record status <review-record-id>
```

Create a review record from a checked-out PR:

```sh
agentics challenge-creator review-record create \
  --repo-url <repo-url> \
  --pr-number <pull-request-number> \
  --pr-url <pull-request-url> \
  --commit-sha <40-hex-git-commit> \
  --repo-dir <checked-out-repo> \
  --challenge-path challenges/<challenge-name> \
  --pr-author-github-user-id <numeric-github-user-id>
```

Upload private ZIP overlays after the review record exists:

```sh
agentics challenge-creator review-record upload-private-asset <review-record-id> \
  --asset-name official-cases \
  --kind private_benchmark_data \
  --file official-cases.zip \
  --required

agentics challenge-creator review-record status <review-record-id>
```

## Local Validation

Run:

```sh
agentics challenge-creator check .
```

This CLI check uses the same Rust contract validation path as the Agentics review workflow. It verifies proposal manifests, public bundle specs, public validation run/session manifests, required-nullable source fields, public `source_path` files, challenge directory/name agreement, and obvious private-data leaks. Agentics server-side validation remains the authoritative publish gate.

## Test Solutions

Public smoke-test solutions live under `test-solutions/<challenge-name>/`.
Each directory is a standalone `zip_project` solution workspace for the challenge with the same handle.

## Thanks

The initial 247 challenges were seeded by porting the non-security problems of [FrontierCS](https://github.com/FrontierCS/Frontier-CS). Huge thanks to the FrontierCS team for their wonderful work on those problems and for open-sourcing them under [the MIT License](https://github.com/FrontierCS/Frontier-CS/blob/main/LICENSE).

## License

Unless a file says otherwise, this repository is licensed under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE).

Some seeded challenge material was derived from [FrontierCS](https://github.com/FrontierCS/Frontier-CS), which is licensed under the MIT License. Keep source attribution in challenge notes when a challenge is ported or adapted from an upstream benchmark.
