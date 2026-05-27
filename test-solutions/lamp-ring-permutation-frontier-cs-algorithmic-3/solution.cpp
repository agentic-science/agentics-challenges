#include <bits/stdc++.h>
using namespace std;

namespace {
constexpr int MAX_EXACT_N = 1000;

vector<int> identity_answer(int n) {
    vector<int> answer(n);
    iota(answer.begin(), answer.end(), 1);
    return answer;
}

vector<int> recover_cycle(int n) {
    vector<vector<int>> neighbors(n + 1);
    long long pairs = 1LL * n * (n - 1) / 2;
    long long operations = 4 * pairs;

    cout << operations;
    for (int a = 1; a <= n; ++a) {
        for (int b = a + 1; b <= n; ++b) {
            cout << ' ' << a << ' ' << b << ' ' << a << ' ' << b;
        }
    }
    cout << endl;

    for (int a = 1; a <= n; ++a) {
        for (int b = a + 1; b <= n; ++b) {
            int first = 0, second = 0, third = 0, fourth = 0;
            if (!(cin >> first >> second >> third >> fourth)) {
                return identity_answer(n);
            }
            (void)first;
            (void)third;
            (void)fourth;
            if (second == 1) {
                neighbors[a].push_back(b);
                neighbors[b].push_back(a);
            }
        }
    }

    if (n == 1) {
        return {1};
    }
    for (int value = 1; value <= n; ++value) {
        if (neighbors[value].size() != 2) {
            return identity_answer(n);
        }
    }

    vector<int> order;
    vector<char> used(n + 1, 0);
    int previous = 0;
    int current = 1;
    while ((int)order.size() < n) {
        order.push_back(current);
        used[current] = 1;
        int next = neighbors[current][0] == previous ? neighbors[current][1] : neighbors[current][0];
        previous = current;
        current = next;
        if ((int)order.size() < n && (current < 1 || current > n || used[current])) {
            return identity_answer(n);
        }
    }
    return order;
}

void print_answer(const vector<int>& answer) {
    cout << -1;
    for (int value : answer) {
        cout << ' ' << value;
    }
    cout << endl;
}
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int subtask = 0;
    int n = 0;
    while (cin >> subtask >> n) {
        if (subtask == 0 && n == 0) {
            return 0;
        }
        if (n <= MAX_EXACT_N) {
            print_answer(recover_cycle(n));
        } else {
            print_answer(identity_answer(n));
        }
    }
    return 0;
}
