#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

using namespace std;

namespace {

using u64 = unsigned long long;
using i128 = __int128_t;

constexpr int MAX_QUESTIONS = 53;

i128 floor_div(i128 value, i128 divisor) {
    if (value >= 0) return value / divisor;
    return -((-value + divisor - 1) / divisor);
}

long long clamp_ll(long long value, long long low, long long high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

string ask(const vector<int>& values) {
    cout << "? " << values.size();
    for (int value : values) cout << ' ' << value;
    cout << '\n' << flush;
    string response;
    if (!(cin >> response)) exit(0);
    return response;
}

bool guess(int value) {
    cout << "! " << value << '\n' << flush;
    string response;
    if (!(cin >> response)) exit(0);
    return response == ":)";
}

void solve_case(int n) {
    vector<u64> truthful_capacity(MAX_QUESTIONS + 1), lied_capacity(MAX_QUESTIONS + 1);
    truthful_capacity[0] = 1;
    lied_capacity[0] = 1;
    for (int remaining = 1; remaining <= MAX_QUESTIONS; ++remaining) {
        lied_capacity[remaining] = truthful_capacity[remaining - 1];
        truthful_capacity[remaining] = truthful_capacity[remaining - 1] + lied_capacity[remaining - 1];
    }

    vector<int> truthful_candidates(n), lied_candidates;
    iota(truthful_candidates.begin(), truthful_candidates.end(), 1);

    vector<int> in_query(n + 1, 0);
    int query_token = 0;
    int asked = 0;

    while (asked < MAX_QUESTIONS && truthful_candidates.size() + lied_candidates.size() > 2) {
        int remaining_after_query = MAX_QUESTIONS - asked - 1;
        u64 truthful_weight = truthful_capacity[remaining_after_query];
        u64 lied_weight = lied_capacity[remaining_after_query];
        u64 truthful_delta = truthful_weight - lied_weight;

        long long count_truthful = static_cast<long long>(truthful_candidates.size());
        long long count_lied = static_cast<long long>(lied_candidates.size());

        i128 total = static_cast<i128>(count_truthful + count_lied) * truthful_weight
            + static_cast<i128>(count_truthful) * lied_weight;
        i128 target = total / 2;
        i128 base = static_cast<i128>(count_truthful) * lied_weight;

        long long approximate_lied_yes = 0;
        if (truthful_weight != 0) {
            approximate_lied_yes = static_cast<long long>(
                floor_div(target - base, static_cast<i128>(truthful_weight))
            );
        }

        vector<long long> lied_yes_candidates;
        lied_yes_candidates.reserve(610);
        lied_yes_candidates.push_back(0);
        lied_yes_candidates.push_back(count_lied);
        for (int delta = -300; delta <= 300; ++delta) {
            lied_yes_candidates.push_back(clamp_ll(approximate_lied_yes + delta, 0, count_lied));
        }
        sort(lied_yes_candidates.begin(), lied_yes_candidates.end());
        lied_yes_candidates.erase(unique(lied_yes_candidates.begin(), lied_yes_candidates.end()), lied_yes_candidates.end());

        i128 best_cost = -1;
        long long best_truthful_yes = 0;
        long long best_lied_yes = 0;

        auto evaluate = [&](long long truthful_yes, long long lied_yes) {
            i128 yes_weight = base
                + static_cast<i128>(lied_yes) * truthful_weight
                + static_cast<i128>(truthful_yes) * truthful_delta;
            i128 no_weight = total - yes_weight;
            i128 cost = max(yes_weight, no_weight);
            if (best_cost < 0 || cost < best_cost) {
                best_cost = cost;
                best_truthful_yes = truthful_yes;
                best_lied_yes = lied_yes;
            }
        };

        for (long long lied_yes : lied_yes_candidates) {
            if (truthful_delta == 0) {
                evaluate(0, lied_yes);
                evaluate(count_truthful, lied_yes);
                continue;
            }

            i128 remainder = target - (base + static_cast<i128>(lied_yes) * truthful_weight);
            long long center = static_cast<long long>(floor_div(remainder, static_cast<i128>(truthful_delta)));
            for (long long option : {center - 2, center - 1, center, center + 1, center + 2, 0LL, count_truthful}) {
                evaluate(clamp_ll(option, 0, count_truthful), lied_yes);
            }
        }

        vector<int> query;
        query.reserve(static_cast<size_t>(best_truthful_yes + best_lied_yes));
        for (long long i = 0; i < best_truthful_yes; ++i) query.push_back(truthful_candidates[static_cast<size_t>(i)]);
        for (long long i = 0; i < best_lied_yes; ++i) query.push_back(lied_candidates[static_cast<size_t>(i)]);

        if (query.empty()) {
            if (!truthful_candidates.empty()) {
                query.push_back(truthful_candidates.front());
            } else if (!lied_candidates.empty()) {
                query.push_back(lied_candidates.front());
            } else {
                break;
            }
        }

        ++query_token;
        for (int value : query) in_query[value] = query_token;

        string response = ask(query);

        vector<int> next_truthful;
        vector<int> next_lied;
        next_truthful.reserve(truthful_candidates.size() + lied_candidates.size());
        next_lied.reserve(truthful_candidates.size());

        if (response == "YES") {
            for (int value : truthful_candidates) {
                if (in_query[value] == query_token) {
                    next_truthful.push_back(value);
                } else {
                    next_lied.push_back(value);
                }
            }
            for (int value : lied_candidates) {
                if (in_query[value] == query_token) next_truthful.push_back(value);
            }
        } else {
            for (int value : truthful_candidates) {
                if (in_query[value] == query_token) {
                    next_lied.push_back(value);
                } else {
                    next_truthful.push_back(value);
                }
            }
            for (int value : lied_candidates) {
                if (in_query[value] != query_token) next_truthful.push_back(value);
            }
        }

        truthful_candidates.swap(next_truthful);
        lied_candidates.swap(next_lied);
        ++asked;
    }

    vector<int> candidates;
    candidates.reserve(truthful_candidates.size() + lied_candidates.size());
    candidates.insert(candidates.end(), truthful_candidates.begin(), truthful_candidates.end());
    candidates.insert(candidates.end(), lied_candidates.begin(), lied_candidates.end());

    if (candidates.empty()) return;
    if (guess(candidates[0])) return;
    if (candidates.size() > 1) guess(candidates[1]);
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
