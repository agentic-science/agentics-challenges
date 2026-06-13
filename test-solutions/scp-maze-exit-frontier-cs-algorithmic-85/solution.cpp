#include <iostream>

using namespace std;

namespace {

constexpr int MOVE_BUDGET = 90000;
constexpr int QUERY_BUDGET = 90000;

int move_count = 0;
int query_count = 0;

int do_move(int color) {
    if (move_count >= MOVE_BUDGET) return -1;
    cout << "move " << color << '\n' << flush;
    int reached = 0;
    if (!(cin >> reached)) return -1;
    ++move_count;
    return reached;
}

int do_query() {
    if (query_count >= QUERY_BUDGET) return -1;
    cout << "query\n" << flush;
    int distance = 0;
    if (!(cin >> distance)) return -1;
    ++query_count;
    return distance;
}

bool solve_case(int initial_deep) {
    int distance = initial_deep;
    move_count = 0;
    query_count = 0;

    while (distance > 0) {
        bool moved_closer = false;
        for (int color = 0; color < 3; ++color) {
            int reached = do_move(color);
            if (reached < 0) return false;
            if (reached == 1) return true;

            int new_distance = do_query();
            if (new_distance < 0) return false;
            if (new_distance < distance) {
                distance = new_distance;
                moved_closer = true;
                break;
            }

            reached = do_move(color);
            if (reached < 0) return false;
            if (reached == 1) return true;
        }

        if (!moved_closer) return false;
    }

    return true;
}

}  // namespace

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int initial_deep = 0;
    while (cin >> initial_deep) {
        if (initial_deep == 0) return 0;
        if (!solve_case(initial_deep)) return 0;
    }

    return 0;
}
