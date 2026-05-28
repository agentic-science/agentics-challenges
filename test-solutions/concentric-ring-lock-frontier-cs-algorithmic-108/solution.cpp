#include <bits/stdc++.h>
using namespace std;

static int n = 0;
static int m = 0;
static int total_sections = 0;
static int current_display = 0;

[[noreturn]] static void stop() {
    exit(0);
}

static int rotate_ring(int ring, int direction) {
    cout << "? " << ring << " " << direction << "\n";
    cout.flush();
    int value = 0;
    if (!(cin >> value)) stop();
    current_display = value;
    return value;
}

static void read_initial_display() {
    rotate_ring(0, 1);
    rotate_ring(0, -1);
}

static vector<int> scan_forward_deltas(int ring, int steps) {
    vector<int> deltas;
    deltas.reserve(steps);
    for (int i = 0; i < steps; ++i) {
        int before = current_display;
        int after = rotate_ring(ring, 1);
        deltas.push_back(after - before);
    }
    return deltas;
}

static void rollback_forward_scan(int ring, int steps) {
    for (int i = 0; i < steps; ++i) rotate_ring(ring, -1);
}

static vector<int> reconstruct_uncovered_without_ring(const vector<int>& deltas) {
    vector<int> values(total_sections, 0);

    for (int residue = 0; residue < m; ++residue) {
        bool found = false;
        vector<int> chosen;

        for (int initial : {0, 1}) {
            int cur = initial;
            bool ok = true;
            vector<int> cycle;
            cycle.reserve(n);

            for (int block = 0; block < n; ++block) {
                int pos = residue + block * m;
                cycle.push_back(cur);
                cur -= deltas[pos];
                if (cur != 0 && cur != 1) ok = false;
            }
            if (cur != initial) ok = false;

            if (ok) {
                chosen = cycle;
                found = true;
                break;
            }
        }

        if (!found) stop();
        for (int block = 0; block < n; ++block) {
            values[residue + block * m] = chosen[block];
        }
    }

    return values;
}

static int align_by_overlap(const vector<int>& reference, const vector<int>& candidate_relative) {
    int best_shift = 0;
    int best_overlap = -1;

    for (int shift = 0; shift < total_sections; ++shift) {
        int overlap = 0;
        for (int pos = 0; pos < total_sections; ++pos) {
            int candidate_index = pos - shift;
            if (candidate_index < 0) candidate_index += total_sections;
            if (reference[pos] && candidate_relative[candidate_index]) ++overlap;
        }
        if (overlap > best_overlap) {
            best_overlap = overlap;
            best_shift = shift;
        }
    }

    return best_shift;
}

static vector<int> shifted_to_reference_frame(const vector<int>& relative, int shift) {
    vector<int> shifted(total_sections, 0);
    for (int pos = 0; pos < total_sections; ++pos) {
        int idx = pos - shift;
        if (idx < 0) idx += total_sections;
        shifted[pos] = relative[idx];
    }
    return shifted;
}

static vector<int> doubled_prefix(const vector<int>& values) {
    vector<int> prefix(2 * total_sections + 1, 0);
    for (int i = 0; i < 2 * total_sections; ++i) {
        prefix[i + 1] = prefix[i] + values[i % total_sections];
    }
    return prefix;
}

static int circular_arc_sum(const vector<int>& prefix, int start, int length) {
    return prefix[start + length] - prefix[start];
}

static int locate_ring_start(const vector<int>& observed, const vector<int>& global_uncovered, const vector<int>& prefix) {
    int best_shift = 0;
    int best_score = INT_MAX;

    for (int shift = 0; shift < total_sections; ++shift) {
        int score = 0;
        if (circular_arc_sum(prefix, shift, m) != 0) score += 1000;

        for (int t = 0; t < (int)observed.size(); ++t) {
            int left = (shift + t) % total_sections;
            int right = (shift + t + m) % total_sections;
            int delta = observed[t];

            if (t < m) {
                int inferred_left = delta + global_uncovered[right];
                if (inferred_left != 0 && inferred_left != 1) ++score;
            } else if (delta != global_uncovered[left] - global_uncovered[right]) {
                ++score;
            }
        }

        if (score < best_score) {
            best_score = score;
            best_shift = shift;
        }
    }

    return best_shift;
}

static void solve_case() {
    total_sections = n * m;
    current_display = 0;

    read_initial_display();

    vector<int> scan0 = scan_forward_deltas(0, total_sections);
    vector<int> without0 = reconstruct_uncovered_without_ring(scan0);

    vector<int> offsets(n, 0);
    if (n >= 2) {
        vector<int> scan1 = scan_forward_deltas(1, total_sections);
        vector<int> without1_relative = reconstruct_uncovered_without_ring(scan1);

        int ring1_shift = align_by_overlap(without0, without1_relative);
        offsets[1] = ring1_shift;

        vector<int> without1 = shifted_to_reference_frame(without1_relative, ring1_shift);
        vector<int> global_uncovered(total_sections, 0);
        for (int pos = 0; pos < total_sections; ++pos) {
            global_uncovered[pos] = without0[pos] && without1[pos] ? 1 : 0;
        }

        vector<int> prefix = doubled_prefix(global_uncovered);
        const int fingerprint_steps = min(total_sections, max(m + 1, 120));

        for (int ring = 2; ring < n; ++ring) {
            vector<int> observed = scan_forward_deltas(ring, fingerprint_steps);
            offsets[ring] = locate_ring_start(observed, global_uncovered, prefix);
            rollback_forward_scan(ring, fingerprint_steps);
        }
    }

    cout << "!";
    for (int ring = 1; ring < n; ++ring) cout << " " << offsets[ring] % total_sections;
    cout << "\n";
    cout.flush();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> n >> m) {
        solve_case();
    }
    return 0;
}
