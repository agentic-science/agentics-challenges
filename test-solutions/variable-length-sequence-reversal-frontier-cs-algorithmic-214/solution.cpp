#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
    }

    cout << 3 << '\n';

    vector<pair<int, int>> ops;
    auto do_reverse = [&](int l, int r) {
        ops.push_back({l, r});
        reverse(a.begin() + l, a.begin() + r + 1);
    };

    int left = 1;
    int right = n;
    while (left < right) {
        int pos_left = -1;
        int pos_right = -1;
        for (int i = 1; i <= n; ++i) {
            if (a[i] == left) {
                pos_left = i;
            }
            if (a[i] == right) {
                pos_right = i;
            }
        }

        if (pos_left - left <= right - pos_right) {
            int cur = pos_left;
            while (cur > left) {
                if (cur - 3 >= left) {
                    do_reverse(cur - 3, cur);
                    cur -= 3;
                } else {
                    do_reverse(cur - 1, cur);
                    --cur;
                }
            }
            ++left;
        } else {
            int cur = pos_right;
            while (cur < right) {
                if (cur + 3 <= right) {
                    do_reverse(cur, cur + 3);
                    cur += 3;
                } else {
                    do_reverse(cur, cur + 1);
                    ++cur;
                }
            }
            --right;
        }
    }

    cout << ops.size() << '\n';
    for (auto [l, r] : ops) {
        cout << l << ' ' << r << '\n';
    }

    return 0;
}
