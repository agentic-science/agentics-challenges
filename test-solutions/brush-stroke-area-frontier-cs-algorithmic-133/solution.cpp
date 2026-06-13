#include <bits/stdc++.h>
using namespace std;

const double SIMPSON_EPS = 1e-10;

struct Point {
    double x;
    double y;
};

struct Capsule {
    double x1;
    double y1;
    double x2;
    double y2;
    double len_sq;
    double min_x;
    double max_x;
};

struct Interval {
    double l;
    double r;

    bool operator<(const Interval &other) const {
        return l < other.l;
    }
};

static int n, m;
static double radius_value;
static vector<Point> points;
static vector<Capsule> capsules;

static double union_length_at(double x, const vector<int> &indices) {
    vector<Interval> intervals;
    intervals.reserve(indices.size());
    double r2 = radius_value * radius_value;

    for (int idx : indices) {
        const Capsule &cap = capsules[idx];
        if (x < cap.min_x || x > cap.max_x) continue;

        double y_min = 1e100;
        double y_max = -1e100;
        bool active = false;

        double dx1 = x - cap.x1;
        if (dx1 * dx1 <= r2) {
            double h = sqrt(max(0.0, r2 - dx1 * dx1));
            y_min = min(y_min, cap.y1 - h);
            y_max = max(y_max, cap.y1 + h);
            active = true;
        }

        double dx2 = x - cap.x2;
        if (dx2 * dx2 <= r2) {
            double h = sqrt(max(0.0, r2 - dx2 * dx2));
            y_min = min(y_min, cap.y2 - h);
            y_max = max(y_max, cap.y2 + h);
            active = true;
        }

        if (cap.len_sq > 1e-12) {
            double dx = cap.x2 - cap.x1;
            double dy = cap.y2 - cap.y1;

            if (fabs(dx) > 1e-9) {
                double cross = (x - cap.x1) * dy + cap.y1 * dx;
                double delta = radius_value * sqrt(cap.len_sq);
                double y1 = (cross - delta) / dx;
                double y2 = (cross + delta) / dx;
                double strip_min = min(y1, y2);
                double strip_max = max(y1, y2);

                double proj_base = -(x - cap.x1) * dx;
                double proj_min = -1e100;
                double proj_max = 1e100;
                if (dy > 1e-9) {
                    proj_min = proj_base / dy + cap.y1;
                    proj_max = (proj_base + cap.len_sq) / dy + cap.y1;
                } else if (dy < -1e-9) {
                    proj_max = proj_base / dy + cap.y1;
                    proj_min = (proj_base + cap.len_sq) / dy + cap.y1;
                } else {
                    double projected = (x - cap.x1) * dx;
                    if (projected < -1e-9 || projected > cap.len_sq + 1e-9) {
                        proj_min = 1e100;
                    }
                }

                double rect_min = max(strip_min, proj_min);
                double rect_max = min(strip_max, proj_max);
                if (rect_min <= rect_max) {
                    y_min = min(y_min, rect_min);
                    y_max = max(y_max, rect_max);
                    active = true;
                }
            } else if (fabs(x - cap.x1) <= radius_value) {
                y_min = min(y_min, min(cap.y1, cap.y2));
                y_max = max(y_max, max(cap.y1, cap.y2));
                active = true;
            }
        }

        if (active) {
            intervals.push_back({y_min, y_max});
        }
    }

    if (intervals.empty()) return 0.0;
    sort(intervals.begin(), intervals.end());

    double total = 0.0;
    double cur_l = intervals[0].l;
    double cur_r = intervals[0].r;
    for (size_t i = 1; i < intervals.size(); ++i) {
        if (intervals[i].l > cur_r) {
            total += cur_r - cur_l;
            cur_l = intervals[i].l;
            cur_r = intervals[i].r;
        } else {
            cur_r = max(cur_r, intervals[i].r);
        }
    }
    total += cur_r - cur_l;
    return total;
}

static double adaptive_simpson(
    double l,
    double r,
    double fl,
    double fr,
    double fm,
    const vector<int> &indices,
    int depth
) {
    double mid = 0.5 * (l + r);
    double left_mid = 0.5 * (l + mid);
    double right_mid = 0.5 * (mid + r);

    double flm = union_length_at(left_mid, indices);
    double frm = union_length_at(right_mid, indices);

    double whole = (r - l) / 6.0 * (fl + 4.0 * fm + fr);
    double left = (mid - l) / 6.0 * (fl + 4.0 * flm + fm);
    double right = (r - mid) / 6.0 * (fm + 4.0 * frm + fr);

    if (depth <= 0 || fabs(left + right - whole) < 15.0 * SIMPSON_EPS) {
        return left + right + (left + right - whole) / 15.0;
    }

    vector<int> left_indices;
    vector<int> right_indices;
    left_indices.reserve(indices.size());
    right_indices.reserve(indices.size());
    for (int idx : indices) {
        if (capsules[idx].max_x > l && capsules[idx].min_x < mid) {
            left_indices.push_back(idx);
        }
        if (capsules[idx].max_x > mid && capsules[idx].min_x < r) {
            right_indices.push_back(idx);
        }
    }

    return adaptive_simpson(l, mid, fl, fm, flm, left_indices, depth - 1) +
           adaptive_simpson(mid, r, fm, fr, frm, right_indices, depth - 1);
}

static double integrate_block(double l, double r, const vector<int> &indices) {
    if (indices.empty()) return 0.0;
    double mid = 0.5 * (l + r);
    double fl = union_length_at(l, indices);
    double fr = union_length_at(r, indices);
    double fm = union_length_at(mid, indices);
    return adaptive_simpson(l, r, fl, fr, fm, indices, 28);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n)) return 0;
    points.resize(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> points[i].x >> points[i].y;
    }

    cin >> m;
    capsules.reserve(m);
    vector<pair<int, int>> segments(m);
    for (int i = 0; i < m; ++i) {
        cin >> segments[i].first >> segments[i].second;
    }

    cin >> radius_value;
    double p1, p2, p3, p4;
    cin >> p1 >> p2 >> p3 >> p4;

    if (m == 0) {
        cout << fixed << setprecision(7) << 0.0 << '\n';
        return 0;
    }

    double min_x = 1e100;
    double max_x = -1e100;
    for (auto [u, v] : segments) {
        Capsule cap;
        cap.x1 = points[u].x;
        cap.y1 = points[u].y;
        cap.x2 = points[v].x;
        cap.y2 = points[v].y;
        double dx = cap.x2 - cap.x1;
        double dy = cap.y2 - cap.y1;
        cap.len_sq = dx * dx + dy * dy;
        cap.min_x = min(cap.x1, cap.x2) - radius_value;
        cap.max_x = max(cap.x1, cap.x2) + radius_value;
        min_x = min(min_x, cap.min_x);
        max_x = max(max_x, cap.max_x);
        capsules.push_back(cap);
    }

    if (max_x - min_x < 1e-12) {
        cout << fixed << setprecision(7) << 0.0 << '\n';
        return 0;
    }

    const int block_count = 128;
    double block_size = (max_x - min_x) / block_count;
    double area = 0.0;

    for (int block = 0; block < block_count; ++block) {
        double l = min_x + block * block_size;
        double r = (block + 1 == block_count) ? max_x : min_x + (block + 1) * block_size;

        vector<int> active;
        active.reserve(m);
        for (int i = 0; i < m; ++i) {
            if (capsules[i].max_x > l && capsules[i].min_x < r) {
                active.push_back(i);
            }
        }
        area += integrate_block(l, r, active);
    }

    cout << fixed << setprecision(7) << area << '\n';
    return 0;
}
