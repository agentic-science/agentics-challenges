# Hello World Rust

Submit a Cargo binary project that writes one greeting.

The evaluator creates a file named `name.txt` in the process working directory.
Your program must read that file, then write `hello.txt` in the same directory.
The contents of `hello.txt` must be:

```text
hello <name>
```

One trailing newline is accepted.

## Submission Contract

Your ZIP project must contain a Cargo project at the workspace root, including
`Cargo.toml` and exactly one binary target. It must also contain
`agentics.solution.json`.

The build command should run:

```sh
cargo build --release
```

The evaluator runs your project once with:

```sh
CARGO_TARGET_DIR=/output/target cargo run --release --manifest-path /workspace/Cargo.toml
```

The evaluator expects the release binary to already exist after the build phase.
It measures the binary size and SHA-256 digest before and after `cargo run`.
If the binary changes, the submission fails.

The solution build phase has network access so Cargo can download dependencies.
The evaluator run phase has network access disabled.

## Scoring

Lower is better. The ranking metric is:

```text
artifact_uncompressed_bytes * binary_bytes
```

`artifact_uncompressed_bytes` comes from trusted Agentics submission metadata,
not from files visible in the workspace. `binary_bytes` is the size of the
compiled release binary used by the evaluator.

Public validation uses a deterministic name. Official evaluation generates one
random ASCII alphanumeric name with length from 1 to 32 at runtime.
