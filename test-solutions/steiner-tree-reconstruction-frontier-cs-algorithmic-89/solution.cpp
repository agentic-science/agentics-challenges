#include <bits/stdc++.h>
using namespace std;

const long long SET_SIZE_LIMIT = 3000000LL;
const long long MAX_EXACT_QUERIES = 60000LL;

bool ask_on_path(int u, int v, int w) {
    cout << "? 2 " << w << " " << u << " " << v << "\n" << flush;
    int ans;
    if (!(cin >> ans) || ans == -1) {
        exit(0);
    }
    return ans == 1;
}

void print_star(int n) {
    cout << "!\n";
    for (int v = 2; v <= n; ++v) {
        cout << 1 << " " << v << "\n";
    }
    cout << flush;
}

vector<pair<int, int>> solve_exact(int n) {
    int root = 1;
    vector<vector<char>> on_root_path(n + 1, vector<char>(n + 1, 0));
    vector<int> depth(n + 1, 0);

    on_root_path[root][root] = 1;
    for (int v = 2; v <= n; ++v) {
        int path_len = 2;
        on_root_path[root][v] = 1;
        on_root_path[v][v] = 1;
        for (int w = 1; w <= n; ++w) {
            if (w == root || w == v) {
                continue;
            }
            if (ask_on_path(root, v, w)) {
                on_root_path[w][v] = 1;
                ++path_len;
            }
        }
        depth[v] = path_len - 1;
    }

    vector<pair<int, int>> edges;
    edges.reserve(max(0, n - 1));
    for (int v = 2; v <= n; ++v) {
        int parent = -1;
        int parent_depth = depth[v] - 1;
        for (int candidate = 1; candidate <= n; ++candidate) {
            if (depth[candidate] == parent_depth && on_root_path[candidate][v]) {
                parent = candidate;
                break;
            }
        }
        if (parent == -1) {
            parent = root;
        }
        edges.emplace_back(parent, v);
    }
    return edges;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {
        long long exact_queries = n >= 2 ? 1LL * (n - 1) * max(0, n - 2) : 0LL;
        if (exact_queries > MAX_EXACT_QUERIES || exact_queries * 2 > SET_SIZE_LIMIT) {
            print_star(n);
            continue;
        }

        vector<pair<int, int>> edges = solve_exact(n);
        cout << "!\n";
        for (auto [u, v] : edges) {
            cout << u << " " << v << "\n";
        }
        cout << flush;
    }

    return 0;
}
