#include <initial-conditions.h>
#include <advection.h>
#include <output.h>

#include <Eigen/Dense>

#include <iostream>

using namespace Eigen;
using namespace std;

int main() {
  const int N          = 32;
  const double delta_t = 0.001;
  Vector2d v           = {3.0, 4.0};

  VectorXd u (N * N);

  squareWave (u, N);

  for (int i = 0; i < 10; ++i) {
    cerr << "timestep " << i << ":" << endl;
    frommVanLeer (u, N, v, delta_t);
  }
  
  displayField (u, N);

  return 0;
}
