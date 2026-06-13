#include <cstdio>
#include <vector>
#include <algorithm>
#include <cstdlib>

using namespace std;

const int MAX_DISTANCE_QUERIES = 60000;

int ask(int u, int v) {
    printf("? %d %d\n", u, v);
    fflush(stdout);
    int d;
    if (scanf("%d", &d) != 1) {
        exit(0);
    }
    return d;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    if (3LL * (n - 1) > MAX_DISTANCE_QUERIES) {
        printf("! 1\n");
        fflush(stdout);
        return 0;
    }

    // Step 1: find one endpoint of the diameter by querying from node 1
    vector<int> dist1(n+1, 0);
    for (int v = 2; v <= n; ++v) {
        dist1[v] = ask(1, v);
    }
    int a = 1;
    for (int v = 2; v <= n; ++v) {
        if (dist1[v] > dist1[a]) {
            a = v;
        }
    }

    // Step 2: query from a to all nodes, find the other endpoint b
    vector<int> distA(n+1, 0);
    for (int v = 1; v <= n; ++v) {
        if (v == a) continue;
        distA[v] = ask(a, v);
    }
    int b = 1;
    for (int v = 2; v <= n; ++v) {
        if (distA[v] > distA[b]) {
            b = v;
        }
    }

    // Step 3: query from b to all nodes
    vector<int> distB(n+1, 0);
    for (int v = 1; v <= n; ++v) {
        if (v == b) continue;
        distB[v] = ask(b, v);
    }

    int D = distA[b];  // distance between a and b

    // Step 4: identify nodes on the path from a to b
    vector<int> dist_to_node(D+1, -1);
    for (int v = 1; v <= n; ++v) {
        if (distA[v] + distB[v] == D) {
            dist_to_node[distA[v]] = v;
        }
    }
    for (int i = 0; i <= D; ++i) {
        if (dist_to_node[i] == -1) {
            printf("! %d\n", a);
            fflush(stdout);
            return 0;
        }
    }

    // Step 5: compute size of attachment for each node on the path
    vector<int> size(D+1, 0);
    for (int v = 1; v <= n; ++v) {
        long long d_diff = distA[v] - distB[v];
        long long key = (D + d_diff) / 2;  // must be integer
        // key is distance from a of the attachment point w
        size[key]++;
    }

    // Step 6: compute prefix sums (left side sizes)
    vector<long long> pref(D+2, 0);
    for (int i = 0; i <= D; ++i) {
        pref[i+1] = pref[i] + size[i];
    }
    // pref[i] = sum_{j=0}^{i-1} size[j]  (nodes strictly left of distance i)

    // Step 7: find centroid
    int centroid = -1;
    for (int i = 0; i <= D; ++i) {
        long long left = pref[i];                 // nodes with distA < i
        long long right = n - pref[i] - size[i];  // nodes with distA > i
        if (left <= n/2 && right <= n/2) {
            centroid = dist_to_node[i];
            break;
        }
    }
    if (centroid == -1) {
        centroid = dist_to_node[D / 2];
    }

    printf("! %d\n", centroid);
    fflush(stdout);

    return 0;
}
