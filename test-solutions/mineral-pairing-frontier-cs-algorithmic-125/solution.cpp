#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <utility>
#include <vector>

using namespace std;

namespace {

constexpr int PASSES = 10;
constexpr int MAX_M = 86000;
constexpr int QUERY_LIMIT = 1000000;

int current_count = 0;
int query_count = 0;
vector<unsigned char> present;

int query(int index) {
    cout << "? " << index << '\n' << flush;
    int response;
    if (!(cin >> response)) exit(0);
    present[index] ^= 1;
    current_count = response;
    ++query_count;
    return response;
}

void answer_pair(int a, int b) {
    cout << "! " << a << ' ' << b << '\n' << flush;
}

void solve_case(int n) {
    int m = 2 * n;
    current_count = 0;
    query_count = 0;
    present.assign(m + 1, 0);

    vector<vector<int>> perm(PASSES, vector<int>(m));
    vector<vector<int>> pos(PASSES, vector<int>(m + 1));
    vector<int> base(m);
    iota(base.begin(), base.end(), 1);

    mt19937 rng(712367);
    for (int pass = 0; pass < PASSES; ++pass) {
        perm[pass] = base;
        shuffle(perm[pass].begin(), perm[pass].end(), rng);
        for (int i = 0; i < m; ++i) {
            pos[pass][perm[pass][i]] = i;
        }
    }

    static unsigned char before_partner[PASSES][MAX_M + 1];

    for (int pass = 0; pass < PASSES; ++pass) {
        if (pass % 2 == 0) {
            for (int index : perm[pass]) {
                int before = current_count;
                int after = query(index);
                before_partner[pass][index] = (after > before) ? 1 : 0;
            }
        } else {
            for (int index : perm[pass]) {
                int before = current_count;
                int after = query(index);
                before_partner[pass][index] = (after == before) ? 1 : 0;
            }
        }
    }

    vector<int> left_vertices;
    vector<int> right_vertices;
    left_vertices.reserve(n);
    right_vertices.reserve(n);
    vector<int> left_id(m + 1, 0), right_id(m + 1, 0);

    for (int index = 1; index <= m; ++index) {
        if (before_partner[0][index]) {
            left_id[index] = static_cast<int>(left_vertices.size()) + 1;
            left_vertices.push_back(index);
        } else {
            right_id[index] = static_cast<int>(right_vertices.size()) + 1;
            right_vertices.push_back(index);
        }
    }

    if (static_cast<int>(left_vertices.size()) != n || static_cast<int>(right_vertices.size()) != n) {
        for (int index = 1; index <= m; index += 2) answer_pair(index, index + 1);
        return;
    }

    int code_bits = PASSES - 1;
    int group_count = 1 << code_bits;
    int mask_all = group_count - 1;
    vector<vector<int>> group_left(group_count), group_right(group_count);

    for (int id = 1; id <= n; ++id) {
        int value = left_vertices[id - 1];
        int code = 0;
        for (int pass = 1; pass < PASSES; ++pass) {
            if (before_partner[pass][value]) code |= 1 << (pass - 1);
        }
        group_left[code].push_back(id);
    }

    for (int id = 1; id <= n; ++id) {
        int value = right_vertices[id - 1];
        int code = 0;
        for (int pass = 1; pass < PASSES; ++pass) {
            if (before_partner[pass][value]) code |= 1 << (pass - 1);
        }
        group_right[code].push_back(id);
    }

    vector<vector<int>> adj_left(n + 1), adj_right(n + 1);
    for (int code = 0; code < group_count; ++code) {
        int complement = (~code) & mask_all;
        const auto& left_group = group_left[code];
        const auto& right_group = group_right[complement];
        if (left_group.empty() || right_group.empty()) continue;

        for (int l_id : left_group) {
            int left_value = left_vertices[l_id - 1];
            for (int r_id : right_group) {
                int right_value = right_vertices[r_id - 1];
                bool possible = true;
                for (int pass = 0; pass < PASSES; ++pass) {
                    bool left_is_before = pos[pass][left_value] < pos[pass][right_value];
                    if (static_cast<bool>(before_partner[pass][left_value]) != left_is_before) {
                        possible = false;
                        break;
                    }
                }
                if (possible) {
                    adj_left[l_id].push_back(r_id);
                    adj_right[r_id].push_back(l_id);
                }
            }
        }
    }

    vector<char> matched_left(n + 1, 0), matched_right(n + 1, 0);
    vector<int> remaining_left_degree(n + 1), remaining_right_degree(n + 1);
    vector<pair<int, int>> answers;
    answers.reserve(n);

    queue<pair<int, int>> forced;
    for (int id = 1; id <= n; ++id) {
        remaining_left_degree[id] = static_cast<int>(adj_left[id].size());
        remaining_right_degree[id] = static_cast<int>(adj_right[id].size());
        if (remaining_left_degree[id] == 1) {
            forced.push({0, id});
        }
        if (remaining_right_degree[id] == 1) {
            forced.push({1, id});
        }
    }

    auto mark_match = [&](int l_id, int r_id) {
        matched_left[l_id] = 1;
        matched_right[r_id] = 1;
        answers.push_back({left_vertices[l_id - 1], right_vertices[r_id - 1]});

        for (int next_right : adj_left[l_id]) {
            if (!matched_right[next_right]) {
                --remaining_right_degree[next_right];
                if (remaining_right_degree[next_right] == 1) {
                    forced.push({1, next_right});
                }
            }
        }
        for (int next_left : adj_right[r_id]) {
            if (!matched_left[next_left]) {
                --remaining_left_degree[next_left];
                if (remaining_left_degree[next_left] == 1) {
                    forced.push({0, next_left});
                }
            }
        }
    };

    while (!forced.empty()) {
        auto [side, id] = forced.front();
        forced.pop();

        if (side == 0) {
            int l_id = id;
            if (matched_left[l_id] || remaining_left_degree[l_id] != 1) {
                continue;
            }
            int only_right = 0;
            for (int r_id : adj_left[l_id]) {
                if (!matched_right[r_id]) {
                    only_right = r_id;
                    break;
                }
            }
            if (only_right != 0) {
                mark_match(l_id, only_right);
            }
        } else {
            int r_id = id;
            if (matched_right[r_id] || remaining_right_degree[r_id] != 1) {
                continue;
            }
            int only_left = 0;
            for (int l_id : adj_right[r_id]) {
                if (!matched_left[l_id]) {
                    only_left = l_id;
                    break;
                }
            }
            if (only_left != 0) {
                mark_match(only_left, r_id);
            }
        }
    }

    vector<int> verification_order;
    verification_order.reserve(n);
    for (int l_id = 1; l_id <= n; ++l_id) {
        if (!matched_left[l_id]) {
            verification_order.push_back(l_id);
        }
        sort(adj_left[l_id].begin(), adj_left[l_id].end(), [&](int a, int b) {
            if (remaining_right_degree[a] != remaining_right_degree[b]) {
                return remaining_right_degree[a] < remaining_right_degree[b];
            }
            return a < b;
        });
    }
    sort(verification_order.begin(), verification_order.end(), [&](int a, int b) {
        if (remaining_left_degree[a] != remaining_left_degree[b]) {
            return remaining_left_degree[a] < remaining_left_degree[b];
        }
        return a < b;
    });

    for (int l_id : verification_order) {
        if (matched_left[l_id]) {
            continue;
        }

        int left_value = left_vertices[l_id - 1];
        bool found = false;
        vector<int> removed_nonmatches;

        query(left_value);

        for (int r_id : adj_left[l_id]) {
            if (matched_right[r_id]) {
                continue;
            }
            if (query_count + 2 > QUERY_LIMIT) {
                break;
            }
            int right_value = right_vertices[r_id - 1];
            bool candidate_was_present = present[right_value];
            int before = current_count;
            query(right_value);
            bool same_kind = candidate_was_present ? (current_count < before) : (current_count == before);
            if (same_kind) {
                mark_match(l_id, r_id);
                found = true;
                break;
            }
            removed_nonmatches.push_back(right_value);
        }

        for (int right_value : removed_nonmatches) {
            query(right_value);
        }

        if (!found) {
            query(left_value);
        }
    }

    for (auto [a, b] : answers) answer_pair(a, b);
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {
        solve_case(n);
    }
    return 0;
}
