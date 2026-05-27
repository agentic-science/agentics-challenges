#include <bits/stdc++.h>
using namespace std;

namespace {
constexpr int MAX_WALKS = 50000;

long long walk(long long steps) {
    cout << "walk " << steps << endl;
    long long label = 0;
    if (!(cin >> label)) {
        exit(0);
    }
    return label;
}

void guess(long long length) {
    cout << "guess " << length << endl;
}

bool solve_case(mt19937_64& rng) {
    unordered_map<long long, long long> seen;
    seen.reserve(MAX_WALKS * 2);
    seen.max_load_factor(0.7);

    long long offset = 0;
    long long period = 0;
    int collisions = 0;

    long long label = walk(0);
    seen[label] = offset;

    uniform_int_distribution<long long> dist(1, 1000000000LL);
    for (int i = 1; i < MAX_WALKS; ++i) {
        long long step = dist(rng);
        offset += step;
        label = walk(step);
        auto it = seen.find(label);
        if (it == seen.end()) {
            seen[label] = offset;
            continue;
        }
        long long delta = llabs(offset - it->second);
        if (delta == 0) {
            continue;
        }
        ++collisions;
        period = period == 0 ? delta : std::gcd(period, delta);
        if (collisions >= 8 && 1 <= period && period <= 1000000000LL) {
            break;
        }
    }

    if (!(1 <= period && period <= 1000000000LL)) {
        period = 1;
    }
    guess(period);

    string marker;
    if (!(cin >> marker)) {
        return false;
    }
    if (marker == "NEXT") {
        return true;
    }
    if (marker == "0") {
        string second;
        cin >> second;
        return false;
    }
    return false;
}
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    mt19937_64 rng(20260528);
    while (solve_case(rng)) {
    }
    return 0;
}
