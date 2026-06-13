#include <bits/stdc++.h>
#if defined(__AVX2__)
#include <immintrin.h>
#endif

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;
    const size_t n = s.size();

    vector<int32_t> pref(n + 1);
    for (size_t i = 0; i < n; ++i) {
        pref[i + 1] = pref[i] + (s[i] == '1');
    }

    unsigned long long ans = 0;
    for (int ones = 1;; ++ones) {
        const size_t len = (size_t)ones * (size_t)(ones + 1);
        if (len > n) break;

        const size_t windows = n - len + 1;
        const int32_t *left = pref.data();
        const int32_t *right = pref.data() + len;

#if defined(__AVX2__)
        const __m256i target = _mm256_set1_epi32(ones);
        __m256i acc0 = _mm256_setzero_si256();
        __m256i acc1 = _mm256_setzero_si256();
        __m256i acc2 = _mm256_setzero_si256();
        __m256i acc3 = _mm256_setzero_si256();

        size_t i = 0;
        for (; i + 32 <= windows; i += 32) {
            __m256i l0 = _mm256_loadu_si256((const __m256i *)(left + i));
            __m256i r0 = _mm256_loadu_si256((const __m256i *)(right + i));
            acc0 = _mm256_add_epi32(
                acc0,
                _mm256_srli_epi32(
                    _mm256_cmpeq_epi32(_mm256_sub_epi32(r0, l0), target),
                    31));

            __m256i l1 = _mm256_loadu_si256((const __m256i *)(left + i + 8));
            __m256i r1 = _mm256_loadu_si256((const __m256i *)(right + i + 8));
            acc1 = _mm256_add_epi32(
                acc1,
                _mm256_srli_epi32(
                    _mm256_cmpeq_epi32(_mm256_sub_epi32(r1, l1), target),
                    31));

            __m256i l2 = _mm256_loadu_si256((const __m256i *)(left + i + 16));
            __m256i r2 = _mm256_loadu_si256((const __m256i *)(right + i + 16));
            acc2 = _mm256_add_epi32(
                acc2,
                _mm256_srli_epi32(
                    _mm256_cmpeq_epi32(_mm256_sub_epi32(r2, l2), target),
                    31));

            __m256i l3 = _mm256_loadu_si256((const __m256i *)(left + i + 24));
            __m256i r3 = _mm256_loadu_si256((const __m256i *)(right + i + 24));
            acc3 = _mm256_add_epi32(
                acc3,
                _mm256_srli_epi32(
                    _mm256_cmpeq_epi32(_mm256_sub_epi32(r3, l3), target),
                    31));
        }

        __m256i acc = _mm256_add_epi32(_mm256_add_epi32(acc0, acc1), _mm256_add_epi32(acc2, acc3));
        for (; i + 8 <= windows; i += 8) {
            __m256i l = _mm256_loadu_si256((const __m256i *)(left + i));
            __m256i r = _mm256_loadu_si256((const __m256i *)(right + i));
            acc = _mm256_add_epi32(
                acc,
                _mm256_srli_epi32(
                    _mm256_cmpeq_epi32(_mm256_sub_epi32(r, l), target),
                    31));
        }

        alignas(32) uint32_t partial[8];
        _mm256_store_si256((__m256i *)partial, acc);
        for (uint32_t value : partial) ans += value;
        for (; i < windows; ++i) ans += (right[i] - left[i]) == ones;
#else
        size_t i = 0;
        for (; i + 8 <= windows; i += 8) {
            ans += (right[i] - left[i]) == ones;
            ans += (right[i + 1] - left[i + 1]) == ones;
            ans += (right[i + 2] - left[i + 2]) == ones;
            ans += (right[i + 3] - left[i + 3]) == ones;
            ans += (right[i + 4] - left[i + 4]) == ones;
            ans += (right[i + 5] - left[i + 5]) == ones;
            ans += (right[i + 6] - left[i + 6]) == ones;
            ans += (right[i + 7] - left[i + 7]) == ones;
        }
        for (; i < windows; ++i) ans += (right[i] - left[i]) == ones;
#endif
    }

    cout << ans << '\n';
    return 0;
}
