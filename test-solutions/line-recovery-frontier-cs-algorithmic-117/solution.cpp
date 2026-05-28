#include <bits/stdc++.h>
using namespace std;

using ld = long double;

constexpr long long X = 20001;
constexpr long long COEFF_LIMIT = 10000;
constexpr long long SEARCH_LIMIT = X * COEFF_LIMIT + COEFF_LIMIT + 5;
constexpr ld KINK_EPS = 1e-7L;

map<long long, ld> cache_values;

ld query_value(long long y) {
    auto cached = cache_values.find(y);
    if (cached != cache_values.end()) return cached->second;

    cout << "? " << X << ' ' << y << endl;
    ld value = 0;
    if (!(cin >> value)) exit(0);
    cache_values.emplace(y, value);
    return value;
}

ld second_difference(long long y) {
    return query_value(y - 1) - 2.0L * query_value(y) + query_value(y + 1);
}

ld discrete_derivative(long long y) {
    return query_value(y + 1) - query_value(y);
}

void find_kinks(long long left, long long right, ld d_left, ld d_right, vector<long long> &kinks) {
    if (d_right - d_left < KINK_EPS) {
        return;
    }

    if (right - left <= 1) {
        kinks.push_back(right);
        return;
    }

    long long mid = left + (right - left) / 2;
    ld d_mid = discrete_derivative(mid);
    find_kinks(left, mid, d_left, d_mid, kinks);
    find_kinks(mid, right, d_mid, d_right, kinks);
}

pair<int, int> decode_line(long long kink) {
    for (long long a = kink / X - 2; a <= kink / X + 2; ++a) {
        long long b = kink - a * X;
        if (-COEFF_LIMIT <= a && a <= COEFF_LIMIT && -COEFF_LIMIT <= b && b <= COEFF_LIMIT) {
            return {int(a), int(b)};
        }
    }
    return {0, int(kink)};
}

void solve_case(int n) {
    cache_values.clear();

    vector<long long> kinks;
    long long left = -SEARCH_LIMIT;
    long long right = SEARCH_LIMIT;
    find_kinks(left, right, discrete_derivative(left), discrete_derivative(right), kinks);
    sort(kinks.begin(), kinks.end());
    kinks.erase(unique(kinks.begin(), kinks.end()), kinks.end());

    vector<pair<int, int>> lines;
    for (long long kink : kinks) {
        auto [a, b] = decode_line(kink);
        ld delta = second_difference(kink);
        ld scale = sqrtl(ld(a) * ld(a) + 1.0L);
        int multiplicity = max(1, int(llround(delta * scale / 2.0L)));
        for (int i = 0; i < multiplicity; ++i) {
            lines.push_back({a, b});
        }
    }

    sort(lines.begin(), lines.end());
    if ((int)lines.size() > n) lines.resize(n);
    while ((int)lines.size() < n) lines.push_back({0, 0});

    cout << "!";
    for (auto [a, _b] : lines) cout << ' ' << a;
    for (auto [_a, b] : lines) cout << ' ' << b;
    cout << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << fixed << setprecision(20);

    int n = 0;
    while (cin >> n) {
        solve_case(n);
    }
    return 0;
}
