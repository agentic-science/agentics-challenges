# N-Body Random 100K Baseline

Uses a per-step spatial grid keyed by the cull radius, then computes the exact provided force/update model against particles in neighboring cells. This keeps the source correctness contract while avoiding the O(N²) naive implementation on official-sized random data.
