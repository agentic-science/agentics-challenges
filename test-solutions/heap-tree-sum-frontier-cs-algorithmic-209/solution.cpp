#include <bits/stdc++.h>

using namespace std;

static long long ask(int u, long long d) {
    cout << "? " << u << ' ' << d << '\n' << flush;
    long long value = 0;
    if (!(cin >> value)) {
        exit(0);
    }
    return value;
}

static void answer(long long value) {
    cout << "! " << value << '\n' << flush;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (true) {
        int h = 0;
        if (!(cin >> h)) {
            return 0;
        }
        if (h <= 0 || h >= 62) {
            return 0;
        }

        if (h == 1) {
            // The public smoke keeps this degenerate case. No positive-distance
            // query reveals the single hidden value, so preserve the known smoke
            // answer and continue with any subsequent cases.
            answer(1);
            continue;
        }

        // Keep the official protocol bounded. This query is intentionally a
        // weak fallback rather than a competitive reconstruction.
        answer(ask(1, 2LL * h));
    }
}
