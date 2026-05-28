#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <unordered_set>
#include <vector>

using namespace std;

namespace {

constexpr int QUERY_LIMIT = 4269;
constexpr int SAMPLE_PIVOTS = 12;
constexpr int SAMPLE_PROBES = 8;

int n = 0;
int queries_used = 0;
vector<vector<int>> cache;

int bit_count(int value) {
    return __builtin_popcount(static_cast<unsigned>(value));
}

int full_value_mask() {
    int mask = 1;
    while (mask < n) {
        mask <<= 1;
    }
    return mask - 1;
}

int query_raw(int i, int j) {
    cout << "? " << i << ' ' << j << '\n' << flush;
    int value = -1;
    if (!(cin >> value)) {
        exit(0);
    }
    if (value == -1) {
        exit(0);
    }
    ++queries_used;
    return value;
}

int ask(int i, int j) {
    if (i == j) {
        return -1;
    }
    if (i > j) {
        swap(i, j);
    }
    int &stored = cache[i][j];
    if (stored == -1) {
        stored = query_raw(i, j);
    }
    return stored;
}

vector<int> shuffled_indices(mt19937 &rng) {
    vector<int> values(n);
    iota(values.begin(), values.end(), 1);
    shuffle(values.begin(), values.end(), rng);
    return values;
}

int choose_pivot(mt19937 &rng) {
    vector<int> order = shuffled_indices(rng);
    int pivot_count = min(n, SAMPLE_PIVOTS);
    int probe_count = min(n - 1, SAMPLE_PROBES);
    int best_pivot = order.front();
    int best_popcount = numeric_limits<int>::max();

    for (int attempt = 0; attempt < pivot_count; ++attempt) {
        int pivot = order[attempt];
        vector<int> probes = shuffled_indices(rng);
        int mask_estimate = full_value_mask();
        int used = 0;
        for (int probe : probes) {
            if (probe == pivot) {
                continue;
            }
            mask_estimate &= ask(pivot, probe);
            ++used;
            if (used == probe_count) {
                break;
            }
        }

        int estimate_popcount = bit_count(mask_estimate);
        if (estimate_popcount < best_popcount) {
            best_popcount = estimate_popcount;
            best_pivot = pivot;
        }
        if (best_popcount <= 4) {
            break;
        }
    }

    return best_pivot;
}

int recover_pivot_value(int pivot, vector<int> &or_with_pivot) {
    int full_mask = full_value_mask();
    int pivot_value = full_mask;
    for (int i = 1; i <= n; ++i) {
        if (i == pivot) {
            continue;
        }
        int value = ask(pivot, i);
        or_with_pivot[i] = value;
        pivot_value &= value;
    }
    return pivot_value;
}

int find_zero_index(int pivot, int pivot_value, const vector<int> &or_with_pivot) {
    if (pivot_value == 0) {
        return pivot;
    }

    vector<int> candidates;
    for (int i = 1; i <= n; ++i) {
        if (i != pivot && or_with_pivot[i] == pivot_value) {
            candidates.push_back(i);
        }
    }
    if (candidates.size() <= 1) {
        return candidates.empty() ? pivot : candidates.front();
    }

    vector<int> references;
    references.reserve(n);
    unordered_set<int> candidate_set(candidates.begin(), candidates.end());
    for (int i = 1; i <= n; ++i) {
        if (i == pivot || candidate_set.find(i) != candidate_set.end()) {
            continue;
        }
        references.push_back(i);
    }
    sort(references.begin(), references.end(), [&](int lhs, int rhs) {
        int lhs_outside = bit_count(or_with_pivot[lhs] & ~pivot_value);
        int rhs_outside = bit_count(or_with_pivot[rhs] & ~pivot_value);
        if (lhs_outside != rhs_outside) {
            return lhs_outside > rhs_outside;
        }
        return or_with_pivot[lhs] > or_with_pivot[rhs];
    });

    if (references.empty()) {
        for (int i = 1; i <= n; ++i) {
            if (i != pivot) {
                references.push_back(i);
            }
        }
    }

    size_t next_reference = 0;
    while (candidates.size() > 1 && next_reference < references.size()) {
        int remaining_after_final_recovery = n - 1;
        if (queries_used + static_cast<int>(candidates.size()) + remaining_after_final_recovery > QUERY_LIMIT) {
            break;
        }

        int reference = references[next_reference++];
        int best_mask = numeric_limits<int>::max();
        vector<pair<int, int>> seen;
        seen.reserve(candidates.size());
        for (int candidate : candidates) {
            if (candidate == reference) {
                continue;
            }
            int masked = ask(candidate, reference) & pivot_value;
            best_mask = min(best_mask, masked);
            seen.push_back({candidate, masked});
        }

        vector<int> narrowed;
        for (auto [candidate, masked] : seen) {
            if (masked == best_mask) {
                narrowed.push_back(candidate);
            }
        }
        if (!narrowed.empty() && narrowed.size() < candidates.size()) {
            candidates.swap(narrowed);
        }
    }

    return candidates.front();
}

bool is_permutation(const vector<int> &values) {
    vector<int> seen(n, 0);
    for (int i = 1; i <= n; ++i) {
        int value = values[i];
        if (value < 0 || value >= n || seen[value]) {
            return false;
        }
        seen[value] = 1;
    }
    return true;
}

void solve_case() {
    queries_used = 0;
    cache.assign(n + 1, vector<int>(n + 1, -1));

    mt19937 rng(0x82B17E5u);
    int pivot = choose_pivot(rng);

    vector<int> or_with_pivot(n + 1, -1);
    int pivot_value = recover_pivot_value(pivot, or_with_pivot);
    int zero_index = find_zero_index(pivot, pivot_value, or_with_pivot);

    vector<int> answer(n + 1, -1);
    answer[zero_index] = 0;
    for (int i = 1; i <= n; ++i) {
        if (i == zero_index) {
            continue;
        }
        answer[i] = ask(zero_index, i);
    }

    if (!is_permutation(answer)) {
        exit(0);
    }

    cout << '!';
    for (int i = 1; i <= n; ++i) {
        cout << ' ' << answer[i];
    }
    cout << '\n' << flush;
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> n) {
        if (n <= 0) {
            break;
        }
        solve_case();
    }
    return 0;
}
