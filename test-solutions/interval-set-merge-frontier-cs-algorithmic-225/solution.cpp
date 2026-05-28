#include <bits/stdc++.h>
using namespace std;

struct Node {
    int lo = 0;
    int hi = 0;
    int left = 0;
    int right = 0;
    vector<int> pref;
    unordered_map<uint64_t, int> memo;
};

int n, q;
vector<int> a;
vector<int> inv_pos;
vector<Node> nodes;
vector<pair<int, int>> ops;
int set_count = 0;

uint64_t pack_key(int left, int right) {
    return (uint64_t(uint32_t(left)) << 32) | uint32_t(right);
}

int build_wavelet(int lo, int hi, const vector<int> &arr) {
    Node node;
    node.lo = lo;
    node.hi = hi;
    node.pref.assign(arr.size() + 1, 0);

    if (lo == hi) {
        nodes.push_back(move(node));
        return int(nodes.size()) - 1;
    }

    int mid = (lo + hi) / 2;
    vector<int> left_values;
    vector<int> right_values;
    left_values.reserve(arr.size());
    right_values.reserve(arr.size());

    for (size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] <= mid) {
            left_values.push_back(arr[i]);
            node.pref[i + 1] = node.pref[i] + 1;
        } else {
            right_values.push_back(arr[i]);
            node.pref[i + 1] = node.pref[i];
        }
    }

    node.left = build_wavelet(lo, mid, left_values);
    node.right = build_wavelet(mid + 1, hi, right_values);
    nodes.push_back(move(node));
    return int(nodes.size()) - 1;
}

int build_interval_set(int node_id, int left, int right) {
    if (left > right) return 0;

    Node &node = nodes[node_id];
    uint64_t key = pack_key(left, right);
    auto cached = node.memo.find(key);
    if (cached != node.memo.end()) return cached->second;

    int result = 0;
    if (node.lo == node.hi) {
        result = inv_pos[node.lo];
    } else {
        int left_l = node.pref[left - 1] + 1;
        int left_r = node.pref[right];
        int right_l = (left - 1) - node.pref[left - 1] + 1;
        int right_r = right - node.pref[right];

        int left_id = left_r >= left_l ? build_interval_set(node.left, left_l, left_r) : 0;
        int right_id = right_r >= right_l ? build_interval_set(node.right, right_l, right_r) : 0;

        if (left_id != 0 && right_id != 0) {
            ops.emplace_back(left_id, right_id);
            result = ++set_count;
        } else {
            result = left_id != 0 ? left_id : right_id;
        }
    }

    node.memo.emplace(key, result);
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n >> q)) return 0;

    a.assign(n + 1, 0);
    inv_pos.assign(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
        inv_pos[a[i]] = i;
    }

    vector<pair<int, int>> queries(q);
    for (auto &[left, right] : queries) {
        cin >> left >> right;
    }

    nodes.reserve(4 * n + 1);
    nodes.push_back(Node{});
    vector<int> values;
    values.reserve(n);
    for (int i = 1; i <= n; ++i) values.push_back(a[i]);

    int root = build_wavelet(1, n, values);
    set_count = n;

    vector<int> answers;
    answers.reserve(q);
    for (auto [left, right] : queries) {
        answers.push_back(build_interval_set(root, left, right));
    }

    cout << set_count << '\n';
    for (auto [left, right] : ops) {
        cout << left << ' ' << right << '\n';
    }
    for (int i = 0; i < q; ++i) {
        if (i > 0) cout << ' ';
        cout << answers[i];
    }
    cout << '\n';
    return 0;
}
