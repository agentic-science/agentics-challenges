#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

using u64 = unsigned long long;
using u128 = unsigned __int128;

int bits(u64 value) {
    if (value == 0) return 0;
    return 64 - __builtin_clzll(value);
}

u64 multiply_mod(u64 left, u64 right, u64 mod) {
    return static_cast<u64>(static_cast<u128>(left) * right % mod);
}

u64 multiply_cost(u64 left, u64 right) {
    return static_cast<u64>(bits(left) + 1) * static_cast<u64>(bits(right) + 1);
}

void solve_case(u64 n) {
    constexpr int BITS = 60;
    constexpr int QUERY_COUNT = 6000;

    mt19937_64 rng(1337);
    uniform_int_distribution<u64> distribution(2, n - 1);

    vector<u64> inputs(QUERY_COUNT);
    vector<long long> residuals(QUERY_COUNT);

    for (int i = 0; i < QUERY_COUNT; ++i) {
        inputs[i] = distribution(rng);
        cout << "? " << inputs[i] << '\n' << flush;
        if (!(cin >> residuals[i])) exit(0);
    }

    vector<vector<u64>> powers(QUERY_COUNT, vector<u64>(BITS));
    for (int row = 0; row < QUERY_COUNT; ++row) {
        u64 value = inputs[row];
        long long base_cost = 0;
        for (int bit = 0; bit < BITS; ++bit) {
            powers[row][bit] = value;
            base_cost += static_cast<long long>(multiply_cost(value, value));
            value = multiply_mod(value, value, n);
        }
        residuals[row] -= base_cost;
    }

    u64 answer = 0;
    vector<u64> result_value(QUERY_COUNT, 1);

    for (int bit = 0; bit < BITS; ++bit) {
        long double sum_x = 0;
        long double sum_y = 0;
        long double sum_xx = 0;
        long double sum_xy = 0;

        for (int row = 0; row < QUERY_COUNT; ++row) {
            long double x = static_cast<long double>(bits(powers[row][bit]) + 1);
            long double y = static_cast<long double>(residuals[row]);
            sum_x += x;
            sum_y += y;
            sum_xx += x * x;
            sum_xy += x * y;
        }

        long double mean_x = sum_x / QUERY_COUNT;
        long double mean_y = sum_y / QUERY_COUNT;
        long double covariance = sum_xy / QUERY_COUNT - mean_x * mean_y;
        long double variance = sum_xx / QUERY_COUNT - mean_x * mean_x;
        long double slope = variance > 1e-12L ? covariance / variance : 0.0L;

        bool bit_is_set = slope > 20.0L;
        if (bit_is_set) {
            answer |= (1ULL << bit);
            for (int row = 0; row < QUERY_COUNT; ++row) {
                residuals[row] -= static_cast<long long>(multiply_cost(result_value[row], powers[row][bit]));
                result_value[row] = multiply_mod(result_value[row], powers[row][bit], n);
            }
        }
    }

    cout << "! " << answer << '\n' << flush;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    u64 n;
    while (cin >> n) {
        solve_case(n);
    }
    return 0;
}
