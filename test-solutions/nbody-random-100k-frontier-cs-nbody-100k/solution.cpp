#include "world.h"
#include <omp.h>
class MySimulator : public Simulator {
public:
  void init(int, StepParameters) override { omp_set_num_threads(2); }
  void simulateStep(std::vector<Particle>& particles, std::vector<Particle>& newParticles, StepParameters params) override {
    #pragma omp parallel for schedule(dynamic, 16)
    for (int i = 0; i < (int)particles.size(); ++i) {
      Particle pi = particles[i]; Vec2 force(0.0f, 0.0f);
      for (size_t j = 0; j < particles.size(); ++j) { if (j != (size_t)i && (pi.position - particles[j].position).length() < params.cullRadius) force += computeForce(pi, particles[j], params.cullRadius); }
      newParticles[i] = updateParticle(pi, force, params.deltaTime);
    }
  }
};
Simulator* createSimulator() { return new MySimulator(); }
