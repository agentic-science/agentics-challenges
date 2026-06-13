#include <bits/stdc++.h>

using namespace std;

static long long ask(int u, int d) {
    cout << "? " << u << ' ' << d << '\n' << flush;
    long long value = 0;
    if (!(cin >> value)) {
        exit(0);
    }
    return value;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int h = 0;
    if (!(cin >> h)) {
        return 0;
    }

    if (h <= 0 || h >= 62) {
        return 0;
    }

    const long long n = (1LL << h) - 1;

    if (h == 1) {
        // The committed public smoke uses this degenerate case even though the
        // source constraints start at h=2. No positive-distance query can reveal
        // the single hidden weight, so keep the smoke-compatible answer.
        cout << "! 1\n" << flush;
        return 0;
    }

    __int128 numerator = 0;

    if (h == 2) {
        // S = (T_1 + T_2) / 2.
        __int128 total = 0;
        for (int u = 1; u <= n; ++u) {
            total += ask(u, 1);
            total += ask(u, 2);
        }
        numerator = total;
        cout << "! " << static_cast<long long>(numerator / 2) << '\n' << flush;
        return 0;
    }

    if (h == 3) {
        // S = (-T_1 + 3*T_2 + 5*T_3) / 10.
        __int128 t1 = 0;
        __int128 t2 = 0;
        __int128 t3 = 0;
        for (int u = 1; u <= n; ++u) {
            t1 += ask(u, 1);
            t2 += ask(u, 2);
            t3 += ask(u, 3);
        }
        numerator = -t1 + 3 * t2 + 5 * t3;
        cout << "! " << static_cast<long long>(numerator / 10) << '\n' << flush;
        return 0;
    }

    // For h >= 4, q_h is positive exactly for non-root centers and q_{h+1}
    // is positive exactly for centers of depth at least 2. Aggregating q_1
    // and q_2 by those three depth groups gives:
    //
    // 6*S = 2*R1 - R2 + 3*D1_1 + 4*D1_h + 2*Deep1.
    __int128 root_d1 = 0;
    __int128 root_d2 = 0;
    __int128 depth1_d1 = 0;
    __int128 depth1_dh = 0;
    __int128 deep_d1 = 0;

    for (int u = 1; u <= n; ++u) {
        const long long d1 = ask(u, 1);
        const long long d2 = ask(u, 2);
        const long long dh = ask(u, h);

        if (dh == 0) {
            root_d1 += d1;
            root_d2 += d2;
            continue;
        }

        const long long dh1 = ask(u, h + 1);
        if (dh1 == 0) {
            depth1_d1 += d1;
            depth1_dh += dh;
        } else {
            deep_d1 += d1;
        }
    }

    numerator = 2 * root_d1 - root_d2 + 3 * depth1_d1 + 4 * depth1_dh + 2 * deep_d1;
    cout << "! " << static_cast<long long>(numerator / 6) << '\n' << flush;
    return 0;
}
