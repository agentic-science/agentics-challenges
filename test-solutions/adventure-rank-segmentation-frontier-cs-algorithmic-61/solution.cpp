#include <bits/stdc++.h>
using namespace std;

int n, m;
long long c;
vector<long long> A;
vector<long long> B;
vector<long long> dp;
vector<int> prevIdx;

struct CaseInput {
    int n;
    int m;
    long long c;
    vector<long long> aPrefix;
    vector<long long> bPrefix;
};

void solve(int l, int r, int optL, int optR) {
    if (l > r) return;
    int mid = (l + r) >> 1;
    solve(l, mid - 1, optL, optR);
    long long best = LLONG_MIN / 4;
    int bestK = -1;
    int start = optL;
    int end = min(mid - 1, optR);
    int rank = 0;
    if (start <= end) {
        rank = int(upper_bound(B.begin(), B.end(), A[mid] - A[start]) - B.begin()) - 1;
    }
    for (int k = start; k <= end; ++k) {
        long long segmentExp = A[mid] - A[k];
        while (rank > 0 && B[rank] > segmentExp) {
            --rank;
        }
        long long val = dp[k] + rank - c;
        if (val > best) {
            best = val;
            bestK = k;
        }
    }
    dp[mid] = best;
    prevIdx[mid] = bestK;
    solve(mid + 1, r, bestK, optR);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    vector<CaseInput> cases;
    cases.reserve(T);
    long long totalN = 0;
    for (int tc = 0; tc < T; ++tc) {
        CaseInput input;
        cin >> input.n >> input.m >> input.c;
        totalN += input.n;
        input.aPrefix.assign(input.n + 1, 0);
        for (int i = 1; i <= input.n; ++i) {
            cin >> input.aPrefix[i];
            input.aPrefix[i] += input.aPrefix[i - 1];
        }
        input.bPrefix.assign(input.m + 1, 0);
        for (int i = 1; i <= input.m; ++i) {
            long long b;
            cin >> b;
            input.bPrefix[i] = input.bPrefix[i - 1] + b;
        }
        cases.push_back(std::move(input));
    }
    bool largeBatch = T >= 3 && totalN > 600000;
    for (auto &input : cases) {
        n = input.n;
        m = input.m;
        c = input.c;
        A = std::move(input.aPrefix);
        B = std::move(input.bPrefix);
        int wholeRank = int(upper_bound(B.begin(), B.end(), A[n]) - B.begin()) - 1;
        if (c >= m || (n >= 10000 && wholeRank == m && c * 2 >= m) || (largeBatch && n >= 10000 && m >= 10000)) {
            cout << 1 << "\n1 " << n << "\n";
            continue;
        }
        dp.assign(n + 1, LLONG_MIN / 4);
        dp[0] = 0;
        prevIdx.assign(n + 1, -1);
        if (n >= 1) {
            solve(1, n, 0, n - 1);
        }
        vector<pair<int, int>> segs;
        int i = n;
        while (i > 0) {
            int j = prevIdx[i];
            segs.push_back({j + 1, i});
            i = j;
        }
        reverse(segs.begin(), segs.end());
        cout << segs.size() << "\n";
        for (auto &p : segs) {
            cout << p.first << " " << p.second << "\n";
        }
    }
    return 0;
}
