#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <utility>
#include <vector>

using namespace std;

namespace {

constexpr int MAX_SIGNATURE_PASSES = 4;
constexpr int QUERY_BUDGET = 120000;
constexpr double TIME_BUDGET_SECONDS = 8.0;

int current_count = 0;
int query_count = 0;

int query(int index) {
    cout << "? " << index << '\n' << flush;
    int response = 0;
    if (!(cin >> response)) exit(0);
    current_count = response;
    ++query_count;
    return response;
}

void answer_pair(int a, int b) {
    cout << "! " << a << ' ' << b << '\n' << flush;
}

bool out_of_time(const chrono::steady_clock::time_point& start_time) {
    chrono::duration<double> elapsed = chrono::steady_clock::now() - start_time;
    return elapsed.count() >= TIME_BUDGET_SECONDS;
}

void answer_adjacent_pairs(int m) {
    for (int index = 1; index <= m; index += 2) {
        answer_pair(index, index + 1);
    }
}

void emit_signature_guess(const vector<vector<unsigned char>>& before_partner, int n) {
    int m = 2 * n;
    int passes = static_cast<int>(before_partner.size());
    if (passes == 0) {
        answer_adjacent_pairs(m);
        return;
    }

    vector<int> left_vertices;
    vector<int> right_vertices;
    left_vertices.reserve(n);
    right_vertices.reserve(n);

    for (int index = 1; index <= m; ++index) {
        if (before_partner[0][index]) {
            left_vertices.push_back(index);
        } else {
            right_vertices.push_back(index);
        }
    }

    if (static_cast<int>(left_vertices.size()) != n || static_cast<int>(right_vertices.size()) != n) {
        answer_adjacent_pairs(m);
        return;
    }

    int code_bits = passes - 1;
    int group_count = 1 << code_bits;
    int mask_all = group_count - 1;
    vector<vector<int>> group_left(group_count), group_right(group_count);

    for (int value : left_vertices) {
        int code = 0;
        for (int pass = 1; pass < passes; ++pass) {
            if (before_partner[pass][value]) code |= 1 << (pass - 1);
        }
        group_left[code].push_back(value);
    }

    for (int value : right_vertices) {
        int code = 0;
        for (int pass = 1; pass < passes; ++pass) {
            if (before_partner[pass][value]) code |= 1 << (pass - 1);
        }
        group_right[code].push_back(value);
    }

    vector<unsigned char> used(m + 1, 0);
    vector<pair<int, int>> answers;
    answers.reserve(n);

    for (int code = 0; code < group_count; ++code) {
        auto& left_group = group_left[code];
        auto& right_group = group_right[(~code) & mask_all];
        size_t pairs = min(left_group.size(), right_group.size());
        for (size_t i = 0; i < pairs; ++i) {
            int left = left_group[i];
            int right = right_group[i];
            used[left] = 1;
            used[right] = 1;
            answers.push_back({left, right});
        }
    }

    vector<int> remaining;
    remaining.reserve(m - 2 * answers.size());
    for (int index = 1; index <= m; ++index) {
        if (!used[index]) remaining.push_back(index);
    }
    for (size_t i = 0; i + 1 < remaining.size() && static_cast<int>(answers.size()) < n; i += 2) {
        answers.push_back({remaining[i], remaining[i + 1]});
    }

    while (static_cast<int>(answers.size()) < n) {
        int first = 2 * static_cast<int>(answers.size()) + 1;
        answers.push_back({first, first + 1});
    }

    for (auto [a, b] : answers) {
        answer_pair(a, b);
    }
}

void solve_case(int n) {
    int m = 2 * n;
    current_count = 0;
    query_count = 0;

    if (m <= 0) return;

    int pass_budget = max(1, QUERY_BUDGET / m);
    int passes_to_run = min(MAX_SIGNATURE_PASSES, pass_budget);

    vector<int> base(m);
    iota(base.begin(), base.end(), 1);
    vector<vector<unsigned char>> before_partner;
    before_partner.reserve(passes_to_run);

    mt19937 rng(712367 + n);
    auto start_time = chrono::steady_clock::now();

    for (int pass = 0; pass < passes_to_run; ++pass) {
        if (query_count + m > QUERY_BUDGET || out_of_time(start_time)) break;

        vector<int> order = base;
        shuffle(order.begin(), order.end(), rng);
        vector<unsigned char> pass_bits(m + 1, 0);

        for (int index : order) {
            if (query_count >= QUERY_BUDGET || out_of_time(start_time)) {
                emit_signature_guess(before_partner, n);
                return;
            }

            int before = current_count;
            int after = query(index);
            pass_bits[index] = (pass % 2 == 0) ? (after > before) : (after == before);
        }

        before_partner.push_back(std::move(pass_bits));
    }

    emit_signature_guess(before_partner, n);
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n = 0;
    while (cin >> n) {
        solve_case(n);
    }

    return 0;
}
