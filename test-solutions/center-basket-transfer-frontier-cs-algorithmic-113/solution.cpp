#include <bits/stdc++.h>
using namespace std;

struct Move {
    unsigned char from;
    unsigned char to;
};

static vector<Move> prefix_moves;

static long long count_t(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    if (n == 2) return 3;
    return 3 * count_t(n - 2) + 4;
}

static long long count_e(int n) {
    if (n <= 1) return 0;
    if (n == 2) return 1;
    if (n == 3) return 2;
    return count_e(n - 2) + 2 + count_t(n - 3);
}

static void add_move(int from, int to) {
    prefix_moves.push_back(Move{static_cast<unsigned char>(from), static_cast<unsigned char>(to)});
}

static void build_t(int n, int source, int target, int aux);
static void build_t_inverse(int n, int source, int target, int aux);

static void build_t(int n, int source, int target, int aux) {
    if (n <= 0) return;
    if (n == 1) {
        add_move(source, target);
        return;
    }
    if (n == 2) {
        add_move(source, aux);
        add_move(source, target);
        add_move(aux, target);
        return;
    }

    build_t(n - 2, source, target, aux);
    add_move(source, aux);
    add_move(source, aux);
    build_t_inverse(n - 2, source, target, aux);
    add_move(aux, target);
    add_move(aux, target);
    build_t(n - 2, source, target, aux);
}

static void build_t_inverse(int n, int source, int target, int aux) {
    if (n <= 0) return;
    if (n == 1) {
        add_move(target, source);
        return;
    }
    if (n == 2) {
        add_move(target, aux);
        add_move(target, source);
        add_move(aux, source);
        return;
    }

    build_t_inverse(n - 2, source, target, aux);
    add_move(target, aux);
    add_move(target, aux);
    build_t(n - 2, source, target, aux);
    add_move(aux, source);
    add_move(aux, source);
    build_t_inverse(n - 2, source, target, aux);
}

static void build_e(int n, int source, int target, int aux) {
    if (n <= 1) return;
    if (n == 2) {
        add_move(source, target);
        return;
    }
    if (n == 3) {
        add_move(source, target);
        add_move(source, target);
        return;
    }

    build_e(n - 2, source, aux, target);
    add_move(source, target);
    add_move(source, target);
    build_t(n - 3, aux, target, source);
}

static int swap_source_target(int basket) {
    if (basket == 1) return 3;
    if (basket == 3) return 1;
    return 2;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long half = count_e(n);
    long long total = 2 * half + 1;
    prefix_moves.reserve(static_cast<size_t>(half));
    build_e(n, 1, 2, 3);

    cout << total << '\n';
    for (const Move &move : prefix_moves) {
        cout << static_cast<int>(move.from) << ' ' << static_cast<int>(move.to) << '\n';
    }
    cout << "1 3\n";
    for (auto it = prefix_moves.rbegin(); it != prefix_moves.rend(); ++it) {
        cout << swap_source_target(static_cast<int>(it->to)) << ' '
             << swap_source_target(static_cast<int>(it->from)) << '\n';
    }

    return 0;
}
