#include "world.h"

#include <algorithm>
#include <cmath>
#include <limits>
#include <omp.h>
#include <vector>

class SpatialGridSimulator : public Simulator {
private:
  float cell_size_ = 1.0f;
  float min_x_ = 0.0f;
  float min_y_ = 0.0f;
  int grid_width_ = 1;
  int grid_height_ = 1;
  std::vector<std::vector<int>> grid_;

  int cell_index(int x, int y) const { return y * grid_width_ + x; }

  int clamp_cell_x(float x) const {
    int cx = static_cast<int>((x - min_x_) / cell_size_);
    return std::clamp(cx, 0, grid_width_ - 1);
  }

  int clamp_cell_y(float y) const {
    int cy = static_cast<int>((y - min_y_) / cell_size_);
    return std::clamp(cy, 0, grid_height_ - 1);
  }

  void build_grid(const std::vector<Particle> &particles, float cull_radius) {
    float max_x = -std::numeric_limits<float>::infinity();
    float max_y = -std::numeric_limits<float>::infinity();
    min_x_ = std::numeric_limits<float>::infinity();
    min_y_ = std::numeric_limits<float>::infinity();

    for (const Particle &particle : particles) {
      min_x_ = std::min(min_x_, particle.position.x);
      min_y_ = std::min(min_y_, particle.position.y);
      max_x = std::max(max_x, particle.position.x);
      max_y = std::max(max_y, particle.position.y);
    }

    cell_size_ = std::max(cull_radius, 1e-6f);
    min_x_ -= cull_radius;
    min_y_ -= cull_radius;
    max_x += cull_radius;
    max_y += cull_radius;

    grid_width_ = std::max(1, static_cast<int>(std::ceil((max_x - min_x_) / cell_size_)) + 1);
    grid_height_ = std::max(1, static_cast<int>(std::ceil((max_y - min_y_) / cell_size_)) + 1);
    grid_.assign(static_cast<size_t>(grid_width_) * static_cast<size_t>(grid_height_), {});

    for (int i = 0; i < static_cast<int>(particles.size()); ++i) {
      int cx = clamp_cell_x(particles[static_cast<size_t>(i)].position.x);
      int cy = clamp_cell_y(particles[static_cast<size_t>(i)].position.y);
      grid_[static_cast<size_t>(cell_index(cx, cy))].push_back(i);
    }
  }

public:
  void init(int, StepParameters) override { omp_set_num_threads(omp_get_max_threads()); }

  void simulateStep(std::vector<Particle> &particles,
                    std::vector<Particle> &newParticles,
                    StepParameters params) override {
    build_grid(particles, params.cullRadius);
    const float radius2 = params.cullRadius * params.cullRadius;

#pragma omp parallel for schedule(dynamic, 64)
    for (int i = 0; i < static_cast<int>(particles.size()); ++i) {
      const Particle &pi = particles[static_cast<size_t>(i)];
      Vec2 force(0.0f, 0.0f);
      int cx = clamp_cell_x(pi.position.x);
      int cy = clamp_cell_y(pi.position.y);

      for (int dy = -1; dy <= 1; ++dy) {
        int ny = cy + dy;
        if (ny < 0 || ny >= grid_height_) {
          continue;
        }
        for (int dx = -1; dx <= 1; ++dx) {
          int nx = cx + dx;
          if (nx < 0 || nx >= grid_width_) {
            continue;
          }
          const std::vector<int> &cell = grid_[static_cast<size_t>(cell_index(nx, ny))];
          for (int j : cell) {
            if (j == i) {
              continue;
            }
            const Particle &pj = particles[static_cast<size_t>(j)];
            if ((pi.position - pj.position).length2() < radius2) {
              force += computeForce(pi, pj, params.cullRadius);
            }
          }
        }
      }

      newParticles[static_cast<size_t>(i)] = updateParticle(pi, force, params.deltaTime);
    }
  }
};

Simulator *createSimulator() { return new SpatialGridSimulator(); }
