#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

using namespace std;

namespace {

constexpr int N = 400;
constexpr int M = 5 * (N - 1);

struct DSU {
    vector<int> parent;
    vector<int> size;

    explicit DSU(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int value) {
        while (parent[value] != value) {
            parent[value] = parent[parent[value]];
            value = parent[value];
        }
        return value;
    }

    bool unite(int left, int right) {
        left = find(left);
        right = find(right);
        if (left == right) return false;
        if (size[left] < size[right]) swap(left, right);
        parent[right] = left;
        size[left] += size[right];
        return true;
    }
};

bool solve_case() {
    int x = 0;
    int y = 0;
    for (int i = 0; i < N; ++i) {
        if (!(cin >> x >> y)) return false;
    }

    vector<pair<int, int>> edges(M);
    for (int i = 0; i < M; ++i) {
        if (!(cin >> edges[i].first >> edges[i].second)) return false;
    }

    DSU accepted(N);
    for (const auto& [u, v] : edges) {
        long long cost = 0;
        if (!(cin >> cost)) return false;
        cout << (accepted.unite(u, v) ? 1 : 0) << '\n' << flush;
    }

    return true;
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (solve_case()) {
    }

    return 0;
}
