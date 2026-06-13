#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <utility>
#include <vector>

using Bits = std::vector<unsigned long long>;

class Solver {
public:
  Solver(int n, int m, std::vector<int> u, std::vector<int> v)
      : n_(n), m_(m), u_(std::move(u)), v_(std::move(v)),
        words_((n + 63) / 64), full_mask_(words_, ~0ULL),
        rng_(seed_from_graph()) {
    if (n_ % 64 != 0) {
      full_mask_.back() = (1ULL << (n_ % 64)) - 1ULL;
    }
  }

  bool solve() {
    if (solve_canonical_path()) {
      return true;
    }
    return solve_by_candidate_filtering();
  }

private:
  int n_;
  int m_;
  std::vector<int> u_;
  std::vector<int> v_;
  int words_;
  std::vector<unsigned long long> full_mask_;
  std::mt19937_64 rng_;

  std::uint64_t seed_from_graph() const {
    std::uint64_t seed = 0x9e3779b97f4a7c15ULL ^ static_cast<std::uint64_t>(n_);
    seed ^= static_cast<std::uint64_t>(m_) << 32;
    for (int i = 0; i < m_; ++i) {
      seed ^= (static_cast<std::uint64_t>(u_[i]) + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2));
      seed ^= (static_cast<std::uint64_t>(v_[i]) + 0xbf58476d1ce4e5b9ULL + (seed << 6) + (seed >> 2));
    }
    return seed;
  }

  int ask(const std::vector<int> &bits) {
    std::cout << 0;
    for (int bit : bits) {
      std::cout << ' ' << bit;
    }
    std::cout << '\n';
    std::cout.flush();

    int reply = -1;
    if (!(std::cin >> reply)) {
      return -1;
    }
    return reply;
  }

  void answer(int a, int b) {
    std::cout << 1 << ' ' << a << ' ' << b << '\n';
    std::cout.flush();
  }

  bool solve_canonical_path() {
    if (m_ != n_ - 1) {
      return false;
    }

    std::vector<int> path_edge(std::max(0, n_ - 1), -1);
    for (int i = 0; i < m_; ++i) {
      if (u_[i] + 1 != v_[i]) {
        return false;
      }
      path_edge[u_[i]] = i;
    }
    if (std::any_of(path_edge.begin(), path_edge.end(), [](int edge) { return edge < 0; })) {
      return false;
    }

    std::vector<int> forward_bits(m_, 0);
    int forward = ask(forward_bits);
    if (forward < 0) {
      return true;
    }

    const bool increasing = forward == 1;
    const int base_bit = increasing ? 0 : 1;
    const int flipped_bit = 1 - base_bit;

    auto query_flipped_range = [&](int left, int right) -> int {
      if (left > right) {
        return 1;
      }
      std::vector<int> bits(m_, base_bit);
      for (int edge_pos = left; edge_pos <= right; ++edge_pos) {
        bits[path_edge[edge_pos]] = flipped_bit;
      }
      return ask(bits);
    };

    int lo = 0;
    int hi = n_ - 2;
    while (lo < hi) {
      int mid = (lo + hi) / 2;
      int reply = query_flipped_range(0, mid);
      if (reply < 0) {
        return true;
      }
      if (reply == 0) {
        hi = mid;
      } else {
        lo = mid + 1;
      }
    }
    int first_edge = lo;

    lo = 0;
    hi = n_ - 1;
    while (lo < hi) {
      int mid = (lo + hi) / 2;
      int reply = query_flipped_range(mid, n_ - 2);
      if (reply < 0) {
        return true;
      }
      if (reply == 0) {
        lo = mid + 1;
      } else {
        hi = mid;
      }
    }
    int last_edge = lo - 1;

    if (increasing) {
      answer(first_edge, last_edge + 1);
    } else {
      answer(last_edge + 1, first_edge);
    }
    return true;
  }

  Bits full_bits() const { return full_mask_; }

  static void set_bit(Bits &bits, int index) {
    bits[static_cast<size_t>(index >> 6)] |= 1ULL << (index & 63);
  }

  static void clear_bit(Bits &bits, int index) {
    bits[static_cast<size_t>(index >> 6)] &= ~(1ULL << (index & 63));
  }

  void and_inplace(Bits &left, const Bits &right) const {
    for (int i = 0; i < words_; ++i) {
      left[static_cast<size_t>(i)] &= right[static_cast<size_t>(i)];
    }
  }

  void and_not_inplace(Bits &left, const Bits &right) const {
    for (int i = 0; i < words_; ++i) {
      left[static_cast<size_t>(i)] &= (~right[static_cast<size_t>(i)]) & full_mask_[static_cast<size_t>(i)];
    }
  }

  void or_inplace(Bits &left, const Bits &right) const {
    for (int i = 0; i < words_; ++i) {
      left[static_cast<size_t>(i)] |= right[static_cast<size_t>(i)];
    }
  }

  void build_orientation(const std::vector<int> &position,
                         std::vector<int> &query_bits,
                         std::vector<Bits> &reachable) const {
    query_bits.assign(static_cast<size_t>(m_), 0);
    std::vector<std::vector<int>> outgoing(static_cast<size_t>(n_));

    for (int i = 0; i < m_; ++i) {
      int a = u_[i];
      int b = v_[i];
      if (position[static_cast<size_t>(a)] > position[static_cast<size_t>(b)]) {
        outgoing[static_cast<size_t>(a)].push_back(b);
        query_bits[static_cast<size_t>(i)] = 0;
      } else {
        outgoing[static_cast<size_t>(b)].push_back(a);
        query_bits[static_cast<size_t>(i)] = 1;
      }
    }

    std::vector<int> order(static_cast<size_t>(n_));
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(), [&](int a, int b) {
      return position[static_cast<size_t>(a)] < position[static_cast<size_t>(b)];
    });

    reachable.assign(static_cast<size_t>(n_), Bits(static_cast<size_t>(words_), 0));
    for (int vertex = 0; vertex < n_; ++vertex) {
      set_bit(reachable[static_cast<size_t>(vertex)], vertex);
    }
    for (int vertex : order) {
      Bits &dsts = reachable[static_cast<size_t>(vertex)];
      for (int next : outgoing[static_cast<size_t>(vertex)]) {
        or_inplace(dsts, reachable[static_cast<size_t>(next)]);
      }
    }
  }

  bool output_if_unique(const std::vector<Bits> &candidates) {
    int found_a = -1;
    int found_b = -1;
    for (int a = 0; a < n_; ++a) {
      for (int word_index = 0; word_index < words_; ++word_index) {
        unsigned long long word = candidates[static_cast<size_t>(a)][static_cast<size_t>(word_index)];
        while (word != 0) {
          int b = word_index * 64 + __builtin_ctzll(word);
          if (b < n_) {
            if (found_a != -1) {
              return false;
            }
            found_a = a;
            found_b = b;
          }
          word &= word - 1;
        }
      }
    }
    if (found_a == -1) {
      return false;
    }
    answer(found_a, found_b);
    return true;
  }

  std::pair<int, int> first_candidate(const std::vector<Bits> &candidates) const {
    for (int a = 0; a < n_; ++a) {
      for (int word_index = 0; word_index < words_; ++word_index) {
        unsigned long long word = candidates[static_cast<size_t>(a)][static_cast<size_t>(word_index)];
        if (word != 0) {
          int b = word_index * 64 + __builtin_ctzll(word);
          if (b < n_) {
            return {a, b};
          }
        }
      }
    }
    return {0, n_ > 1 ? 1 : 0};
  }

  void apply_reply(std::vector<Bits> &candidates, const std::vector<Bits> &reachable, int reply) const {
    for (int a = 0; a < n_; ++a) {
      Bits &row = candidates[static_cast<size_t>(a)];
      if (reply == 1) {
        and_inplace(row, reachable[static_cast<size_t>(a)]);
      } else {
        and_not_inplace(row, reachable[static_cast<size_t>(a)]);
      }
      clear_bit(row, a);
    }
  }

  bool solve_by_candidate_filtering() {
    std::vector<Bits> candidates(static_cast<size_t>(n_), full_bits());
    for (int a = 0; a < n_; ++a) {
      clear_bit(candidates[static_cast<size_t>(a)], a);
    }

    std::vector<int> order(static_cast<size_t>(n_));
    std::iota(order.begin(), order.end(), 0);
    std::vector<int> position(static_cast<size_t>(n_));
    std::vector<int> query_bits;
    std::vector<Bits> reachable;

    int used = 0;
    while (used < 600) {
      std::shuffle(order.begin(), order.end(), rng_);
      for (int i = 0; i < n_; ++i) {
        position[static_cast<size_t>(order[static_cast<size_t>(i)])] = i;
      }

      build_orientation(position, query_bits, reachable);
      int reply = ask(query_bits);
      if (reply < 0) {
        return true;
      }
      ++used;
      apply_reply(candidates, reachable, reply);
      if (output_if_unique(candidates)) {
        return true;
      }

      if (used >= 600) {
        break;
      }

      for (int vertex = 0; vertex < n_; ++vertex) {
        position[static_cast<size_t>(vertex)] = n_ - 1 - position[static_cast<size_t>(vertex)];
      }
      build_orientation(position, query_bits, reachable);
      reply = ask(query_bits);
      if (reply < 0) {
        return true;
      }
      ++used;
      apply_reply(candidates, reachable, reply);
      if (output_if_unique(candidates)) {
        return true;
      }
    }

    auto [a, b] = first_candidate(candidates);
    answer(a, b);
    return true;
  }
};

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  while (true) {
    int n = 0;
    int m = 0;
    if (!(std::cin >> n >> m)) {
      return 0;
    }

    std::vector<int> u(static_cast<size_t>(m));
    std::vector<int> v(static_cast<size_t>(m));
    for (int i = 0; i < m; ++i) {
      std::cin >> u[static_cast<size_t>(i)] >> v[static_cast<size_t>(i)];
    }

    Solver solver(n, m, std::move(u), std::move(v));
    if (!solver.solve()) {
      return 0;
    }
  }
}
