#! /usr/bin/python

from dolfin import *
import numpy

from initialConditions import *
from utility import *

l1_old = l2_old = linf_old = 1

N = 256
while (N <= 8192):
  mu      = 1.0
  kappa   = 1.0
  t_end   = 0.03125

  h = 1.0 / N

  dt = mu *  h / kappa

  mesh = UnitIntervalMesh(N)
  V = FunctionSpace(mesh, 'Lagrange', 2)

  #u1 = sineWave(kappa, 0)
  u1 = squareWave()

  bc = DirichletBC(V, Constant(0.0), boundary)

  u_1 = interpolate(u1, V)

  u = TrialFunction(V)
  v = TestFunction(V)

  u = TrialFunction(V)
  a = v*u*dx + kappa*dt*inner(nabla_grad(v), nabla_grad(u))*dx
  A = assemble(a)
  u = Function(V)

  t = 0

  while t < t_end:
    L = v*u_1*dx
    b = assemble(L)
    bc.apply(A, b)
    solve(A, u.vector(), b)
    u_1.assign(u)
    plot(u_1, rescale=False)
    interactive()
    t += dt

  M = min(N, 300)

  #u_exact = interpolate(sineWave(kappa, t), V)
  u_exact = interpolate(fourierSquare(M, kappa, t), V)

  u_error = u_1.vector() - u_exact.vector()

  l1   = u_error.norm('l1') / N
  l2   = u_error.norm('l2') / sqrt(N)
  linf = u_error.norm('linf')

  print 'N: {}\tL1: {:.6e}\t{:.2f}\tL2: {:.6e}\t{:.2f}\tLinf: {:.6e}\t{:.2f}'.format(N, l1, numpy.log2(l1_old/l1), l2, numpy.log2(l2_old/l2), linf, numpy.log2(linf_old/linf))

  l1_old   = l1
  l2_old   = l2
  linf_old = linf
  N *= 2
