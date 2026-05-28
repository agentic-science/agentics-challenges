#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
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

    DSU(int n = 0) { init(n); }

    void init(int n) {
        parent.resize(n);
        size.assign(n, 1);
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

    bool same(int left, int right) { return find(left) == find(right); }
};

struct Edge {
    int u;
    int v;
    int d;
};

struct SimEdge {
    int u;
    int v;
    int w;

    bool operator<(const SimEdge& other) const {
        if (w != other.w) return w < other.w;
        if (u != other.u) return u < other.u;
        return v < other.v;
    }
};

uint32_t rng_state = 123456789u;

uint32_t xorshift() {
    uint32_t value = rng_state;
    value ^= value << 13;
    value ^= value >> 17;
    value ^= value << 5;
    rng_state = value;
    return value;
}

int rounded_distance(int x1, int y1, int x2, int y2) {
    long long dx = x1 - x2;
    long long dy = y1 - y2;
    return max(1, static_cast<int>(llround(sqrt(static_cast<double>(dx * dx + dy * dy)))));
}

int path_max(
    int start,
    int goal,
    const vector<vector<pair<int, int>>>& adj,
    vector<int>& queue,
    vector<int>& parent,
    vector<int>& parent_weight,
    vector<int>& seen,
    int& seen_token
) {
    int head = 0;
    int tail = 0;
    queue[tail++] = start;
    ++seen_token;
    seen[start] = seen_token;
    parent[start] = -1;
    parent_weight[start] = 0;

    while (head < tail) {
        int current = queue[head++];
        if (current == goal) break;
        for (auto [next, weight] : adj[current]) {
            if (seen[next] == seen_token) continue;
            seen[next] = seen_token;
            parent[next] = current;
            parent_weight[next] = weight;
            queue[tail++] = next;
        }
    }

    if (seen[goal] != seen_token) return 1'000'000'000;

    int result = 0;
    for (int current = goal; current != start; current = parent[current]) {
        result = max(result, parent_weight[current]);
    }
    return result;
}

bool solve_case() {
    vector<int> x(N), y(N);
    for (int i = 0; i < N; ++i) {
        if (!(cin >> x[i] >> y[i])) return false;
    }

    vector<Edge> edges(M);
    for (int i = 0; i < M; ++i) {
        int u;
        int v;
        cin >> u >> v;
        edges[i] = {u, v, rounded_distance(x[u], y[u], x[v], y[v])};
    }

    DSU accepted(N);
    vector<SimEdge> sim_edges;
    sim_edges.reserve(M);
    vector<vector<pair<int, int>>> adj(N);
    vector<int> queue(N);
    vector<int> parent(N);
    vector<int> parent_weight(N);
    vector<int> seen(N, 0);
    int seen_token = 0;

    auto start_time = chrono::steady_clock::now();
    constexpr double time_limit = 8.5;

    for (int i = 0; i < M; ++i) {
        int length;
        if (!(cin >> length)) return false;

        int u = edges[i].u;
        int v = edges[i].v;
        if (accepted.same(u, v)) {
            cout << 0 << '\n' << flush;
            continue;
        }

        DSU reach = accepted;
        for (int j = i + 1; j < M; ++j) {
            reach.unite(edges[j].u, edges[j].v);
        }
        if (!reach.same(u, v)) {
            cout << 1 << '\n' << flush;
            accepted.unite(u, v);
            continue;
        }

        long long threshold_sum = 0;
        int simulations = 0;

        auto run_simulation = [&](bool mean_field) {
            sim_edges.clear();
            for (int j = i + 1; j < M; ++j) {
                int ru = accepted.find(edges[j].u);
                int rv = accepted.find(edges[j].v);
                if (ru == rv) continue;
                int weight;
                if (mean_field) {
                    weight = 2 * edges[j].d;
                } else {
                    int span = 2 * edges[j].d + 1;
                    weight = edges[j].d + static_cast<int>((static_cast<uint64_t>(xorshift()) * span) >> 32);
                }
                sim_edges.push_back({ru, rv, weight});
            }
            sort(sim_edges.begin(), sim_edges.end());

            DSU future(N);
            for (auto& bucket : adj) bucket.clear();

            int start = accepted.find(u);
            int goal = accepted.find(v);
            for (const auto& edge : sim_edges) {
                if (future.unite(edge.u, edge.v)) {
                    adj[edge.u].push_back({edge.v, edge.w});
                    adj[edge.v].push_back({edge.u, edge.w});
                }
            }

            threshold_sum += path_max(start, goal, adj, queue, parent, parent_weight, seen, seen_token);
            ++simulations;
        };

        run_simulation(true);

        while (true) {
            if ((simulations & 15) == 0) {
                auto now = chrono::steady_clock::now();
                double elapsed = chrono::duration<double>(now - start_time).count();
                if (elapsed >= time_limit) break;
                double budget = (time_limit - elapsed) / max(1, M - i);
                if (budget < 0.00015) break;
            }
            if (simulations >= 96) break;
            run_simulation(false);
        }

        double threshold = static_cast<double>(threshold_sum) / simulations;
        if (length < threshold) {
            cout << 1 << '\n' << flush;
            accepted.unite(u, v);
        } else {
            cout << 0 << '\n' << flush;
        }
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
