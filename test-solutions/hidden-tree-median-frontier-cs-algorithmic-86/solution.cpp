#include <bits/stdc++.h>
using namespace std;

static int n;
static vector<pair<int, int>> edges;
static unordered_map<unsigned long long, int> cache;

static unsigned long long key_for(int a, int b, int c) {
    int x[3] = {a, b, c};
    sort(x, x + 3);
    return (static_cast<unsigned long long>(x[0]) << 22) |
           (static_cast<unsigned long long>(x[1]) << 11) |
           static_cast<unsigned long long>(x[2]);
}

static int median_query(int a, int b, int c) {
    if (a == b || a == c || b == c) return a;
    unsigned long long key = key_for(a, b, c);
    auto it = cache.find(key);
    if (it != cache.end()) return it->second;

    cout << "0 " << a << ' ' << b << ' ' << c << '\n';
    cout.flush();
    int answer;
    if (!(cin >> answer)) exit(0);
    cache.emplace(key, answer);
    return answer;
}

static bool before_on_path(int anchor, int lhs, int rhs) {
    if (lhs == rhs) return false;
    if (lhs == anchor) return true;
    if (rhs == anchor) return false;
    return median_query(anchor, lhs, rhs) == lhs;
}

static pair<int, int> choose_anchors(const vector<int>& nodes) {
    return {nodes.front(), nodes.back()};
}

static void solve_component(vector<int> nodes) {
    if (nodes.size() <= 1) return;
    if (nodes.size() == 2) {
        edges.push_back({nodes[0], nodes[1]});
        return;
    }

    auto [a, b] = choose_anchors(nodes);
    vector<int> path;
    unordered_map<int, vector<int>> attached;
    path.push_back(a);
    path.push_back(b);

    for (int x : nodes) {
        if (x == a || x == b) continue;
        int projection = median_query(a, b, x);
        if (projection == x) {
            path.push_back(x);
        } else {
            attached[projection].push_back(x);
        }
    }

    sort(path.begin(), path.end(), [&](int lhs, int rhs) {
        return before_on_path(a, lhs, rhs);
    });

    for (int i = 0; i + 1 < static_cast<int>(path.size()); ++i) {
        edges.push_back({path[i], path[i + 1]});
    }

    for (int root : path) {
        auto it = attached.find(root);
        if (it == attached.end()) continue;
        vector<int> child_component;
        child_component.reserve(it->second.size() + 1);
        child_component.push_back(root);
        for (int x : it->second) child_component.push_back(x);
        solve_component(move(child_component));
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> n) {
        edges.clear();
        cache.clear();

        vector<int> nodes(n);
        iota(nodes.begin(), nodes.end(), 1);
        solve_component(nodes);

        if (static_cast<int>(edges.size()) != n - 1) {
            vector<int> parent(n + 1);
            iota(parent.begin(), parent.end(), 0);
            function<int(int)> find_parent = [&](int x) {
                return parent[x] == x ? x : parent[x] = find_parent(parent[x]);
            };
            auto unite = [&](int a, int b) {
                a = find_parent(a);
                b = find_parent(b);
                if (a != b) parent[a] = b;
            };
            for (auto [u, v] : edges) unite(u, v);
            for (int v = 2; v <= n && static_cast<int>(edges.size()) < n - 1; ++v) {
                if (find_parent(1) != find_parent(v)) {
                    edges.push_back({1, v});
                    unite(1, v);
                }
            }
            if (static_cast<int>(edges.size()) > n - 1) edges.resize(n - 1);
        }

        cout << "1";
        for (auto [u, v] : edges) cout << ' ' << u << ' ' << v;
        cout << '\n';
        cout.flush();
    }
    return 0;
}
