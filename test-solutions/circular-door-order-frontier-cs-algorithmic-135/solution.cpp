#include <bits/stdc++.h>
using namespace std;

static int K = 0;
static int N = 0;
static long long query_count = 0;
static mt19937 rng(28u);

static void finish_with_identity() {
    cout << "!";
    for (int i = 0; i < N; ++i) cout << " " << i;
    cout << "\n";
    cout.flush();
}

[[noreturn]] static void stop() {
    exit(0);
}

static vector<pair<int, int>> ask(int x, int y, int z) {
    if (x == y || y == z || x == z) stop();
    cout << "? " << x << " " << y << " " << z << "\n";
    cout.flush();
    ++query_count;

    int r = 0;
    if (!(cin >> r)) stop();
    vector<pair<int, int>> res;
    res.reserve(r);
    for (int i = 0; i < r; ++i) {
        int a = 0, b = 0;
        cin >> a >> b;
        if (a > b) swap(a, b);
        res.push_back({a, b});
    }
    return res;
}

static bool contains_pair(const vector<pair<int, int>>& pairs, int a, int b) {
    if (a > b) swap(a, b);
    for (auto [x, y] : pairs) {
        if (x == a && y == b) return true;
    }
    return false;
}

static bool verify_adjacent(int a, int b) {
    for (int c = 0; c < N; ++c) {
        if (c == a || c == b) continue;
        auto res = ask(a, b, c);
        if (!contains_pair(res, a, b)) return false;
    }
    return true;
}

static int randint(int lo, int hi) {
    uniform_int_distribution<int> dist(lo, hi);
    return dist(rng);
}

static int random_vertex() {
    return randint(0, N - 1);
}

static int random_vertex_not(int a) {
    int x = 0;
    do {
        x = random_vertex();
    } while (x == a);
    return x;
}

static int random_vertex_not2(int a, int b) {
    int x = 0;
    do {
        x = random_vertex();
    } while (x == a || x == b);
    return x;
}

static int approximate_farthest_from(int a, int iterations) {
    int b = random_vertex_not(a);
    for (int i = 0; i < iterations; ++i) {
        int c = random_vertex_not2(a, b);
        auto res = ask(a, b, c);
        bool ab = contains_pair(res, a, b);
        bool ac = contains_pair(res, a, c);
        if (ab && !ac) {
            b = c;
        } else if (ab && ac && randint(0, 1) == 1) {
            b = c;
        }
    }
    return b;
}

static bool good_pivot_pair(int a, int b, int checks, int threshold) {
    int bad = 0;
    for (int i = 0; i < checks; ++i) {
        int x = random_vertex_not2(a, b);
        auto res = ask(x, a, b);
        bool xa = contains_pair(res, x, a);
        bool xb = contains_pair(res, x, b);
        bool ab = contains_pair(res, a, b);
        if (ab && !xa && !xb) ++bad;
    }
    return bad <= threshold;
}

static pair<int, int> find_adjacent_pair() {
    vector<int> perm(N);
    iota(perm.begin(), perm.end(), 0);

    for (int attempt = 0; attempt < 8; ++attempt) {
        shuffle(perm.begin(), perm.end(), rng);
        int a = perm[0];
        int b = perm[1];

        for (int i = 2; i < N; ++i) {
            int c = perm[i];
            auto res = ask(a, b, c);
            pair<int, int> chosen = res[0];
            for (auto p : res) {
                if (p.first == c || p.second == c) {
                    chosen = p;
                    break;
                }
            }
            a = chosen.first;
            b = chosen.second;
        }

        if (verify_adjacent(a, b)) return {a, b};
    }

    for (int attempt = 0; attempt < 8; ++attempt) {
        int a = random_vertex();
        int b = random_vertex_not(a);
        vector<int> order(N);
        iota(order.begin(), order.end(), 0);
        shuffle(order.begin(), order.end(), rng);

        for (int c : order) {
            if (c == a || c == b) continue;
            auto res = ask(a, b, c);
            pair<int, int> chosen = res[0];
            for (auto p : res) {
                if (p.first == c || p.second == c) {
                    chosen = p;
                    break;
                }
            }
            a = chosen.first;
            b = chosen.second;
        }

        if (verify_adjacent(a, b)) return {a, b};
    }

    for (int a = 0; a < N; ++a) {
        for (int b = a + 1; b < N; ++b) {
            if (verify_adjacent(a, b)) return {a, b};
        }
    }
    stop();
}

static void solve_case() {
    if (N <= 3) {
        finish_with_identity();
        return;
    }

    auto [start0, start1] = find_adjacent_pair();

    const int signature_count = min(8, max(1, N - 1));
    const int far_iterations = 28;
    const int good_checks = 6;
    const int good_threshold = 2;

    vector<pair<int, int>> pivots;
    pivots.reserve(signature_count);
    for (int i = 0; i < signature_count; ++i) {
        pair<int, int> best = {0, 1};
        bool accepted = false;
        for (int rep = 0; rep < 12 && !accepted; ++rep) {
            int a = random_vertex();
            int b = approximate_farthest_from(a, far_iterations);
            if (a == b) continue;
            best = {a, b};
            if (good_pivot_pair(a, b, good_checks, good_threshold)) accepted = true;
        }
        pivots.push_back(best);
    }

    vector<long long> pow3(signature_count + 1, 1);
    for (int i = 1; i <= signature_count; ++i) pow3[i] = pow3[i - 1] * 3LL;

    vector<vector<uint8_t>> digits(N, vector<uint8_t>(signature_count, 2));
    vector<long long> signature(N, 0);
    for (int x = 0; x < N; ++x) {
        long long value = 0;
        long long mult = 1;
        for (int i = 0; i < signature_count; ++i) {
            int a = pivots[i].first;
            int b = pivots[i].second;
            int d = 2;
            if (x == a) {
                d = 0;
            } else if (x == b) {
                d = 1;
            } else {
                auto res = ask(x, a, b);
                bool xa = contains_pair(res, x, a);
                bool xb = contains_pair(res, x, b);
                if (xa && !xb) d = 0;
                else if (xb && !xa) d = 1;
                else if (xa && xb) d = 0;
            }
            digits[x][i] = static_cast<uint8_t>(d);
            value += mult * d;
            mult *= 3LL;
        }
        signature[x] = value;
    }

    vector<vector<long long>> masked1(N, vector<long long>(signature_count, 0));
    for (int v = 0; v < N; ++v) {
        for (int i = 0; i < signature_count; ++i) {
            long long value = 0;
            long long mult = 1;
            for (int j = 0; j < signature_count; ++j) {
                if (j == i) continue;
                value += mult * digits[v][j];
                mult *= 3LL;
            }
            masked1[v][i] = value;
        }
    }

    vector<pair<int, int>> pair_pos;
    vector<vector<long long>> masked2;
    for (int i = 0; i < signature_count; ++i) {
        for (int j = i + 1; j < signature_count; ++j) pair_pos.push_back({i, j});
    }
    masked2.assign(N, vector<long long>(pair_pos.size(), 0));
    for (int v = 0; v < N; ++v) {
        for (int idx = 0; idx < (int)pair_pos.size(); ++idx) {
            int a = pair_pos[idx].first;
            int b = pair_pos[idx].second;
            long long value = 0;
            long long mult = 1;
            for (int k = 0; k < signature_count; ++k) {
                if (k == a || k == b) continue;
                value += mult * digits[v][k];
                mult *= 3LL;
            }
            masked2[v][idx] = value;
        }
    }

    unordered_map<long long, vector<int>> bucket0;
    unordered_map<long long, vector<int>> bucket1;
    unordered_map<long long, vector<int>> bucket2;
    bucket0.reserve(N * 2);
    bucket1.reserve(N * signature_count * 2);
    bucket2.reserve(N * 4);

    for (int v = 0; v < N; ++v) bucket0[signature[v]].push_back(v);

    long long base1 = pow3[signature_count - 1];
    for (int v = 0; v < N; ++v) {
        for (int i = 0; i < signature_count; ++i) {
            bucket1[(long long)i * base1 + masked1[v][i]].push_back(v);
        }
    }

    long long base2 = pow3[max(0, signature_count - 2)];
    for (int v = 0; v < N; ++v) {
        for (int idx = 0; idx < (int)pair_pos.size(); ++idx) {
            bucket2[(long long)idx * base2 + masked2[v][idx]].push_back(v);
        }
    }

    auto is_neighbor = [&](int cur, int prev, int cand) {
        auto res = ask(cur, prev, cand);
        return contains_pair(res, cur, cand);
    };

    vector<char> used(N, 0);
    vector<int> answer;
    answer.reserve(N);
    answer.push_back(start0);
    answer.push_back(start1);
    used[start0] = 1;
    used[start1] = 1;

    vector<int> seen(N, 0);
    int stamp = 1;

    auto gather_and_try = [&](int prev, int cur, bool two_wildcards) -> int {
        vector<int> candidates;
        candidates.reserve(64);

        auto add_bucket = [&](const vector<int>* bucket) {
            if (bucket == nullptr) return;
            for (int x : *bucket) {
                if (seen[x] == stamp) continue;
                seen[x] = stamp;
                candidates.push_back(x);
            }
        };

        auto it0 = bucket0.find(signature[cur]);
        if (it0 != bucket0.end()) add_bucket(&it0->second);

        for (int i = 0; i < signature_count; ++i) {
            auto it1 = bucket1.find((long long)i * base1 + masked1[cur][i]);
            if (it1 != bucket1.end()) add_bucket(&it1->second);
        }

        if (two_wildcards) {
            for (int idx = 0; idx < (int)pair_pos.size(); ++idx) {
                auto it2 = bucket2.find((long long)idx * base2 + masked2[cur][idx]);
                if (it2 != bucket2.end()) add_bucket(&it2->second);
            }
        }

        for (int candidate : candidates) {
            if (candidate == prev || candidate == cur || used[candidate]) continue;
            if (is_neighbor(cur, prev, candidate)) return candidate;
        }
        return -1;
    };

    auto similarity_fallback = [&](int prev, int cur) -> int {
        vector<pair<int, int>> scored;
        scored.reserve(N);
        for (int candidate = 0; candidate < N; ++candidate) {
            if (candidate == prev || candidate == cur || used[candidate]) continue;
            int score = 0;
            for (int i = 0; i < signature_count; ++i) {
                if (digits[candidate][i] == digits[cur][i]) ++score;
            }
            scored.push_back({-score, candidate});
        }
        sort(scored.begin(), scored.end());
        for (auto [_, candidate] : scored) {
            if (is_neighbor(cur, prev, candidate)) return candidate;
        }
        for (int candidate = 0; candidate < N; ++candidate) {
            if (candidate == prev || candidate == cur || used[candidate]) continue;
            if (is_neighbor(cur, prev, candidate)) return candidate;
        }
        return -1;
    };

    while ((int)answer.size() < N) {
        int prev = answer[(int)answer.size() - 2];
        int cur = answer.back();

        ++stamp;
        if (stamp == INT_MAX) {
            fill(seen.begin(), seen.end(), 0);
            stamp = 1;
        }

        int next = gather_and_try(prev, cur, false);
        if (next == -1) {
            ++stamp;
            if (stamp == INT_MAX) {
                fill(seen.begin(), seen.end(), 0);
                stamp = 1;
            }
            next = gather_and_try(prev, cur, true);
        }
        if (next == -1) next = similarity_fallback(prev, cur);
        if (next < 0) stop();

        used[next] = 1;
        answer.push_back(next);
    }

    cout << "!";
    for (int x : answer) cout << " " << x;
    cout << "\n";
    cout.flush();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> K >> N) {
        query_count = 0;
        rng.seed(28u);
        solve_case();
    }
    return 0;
}
