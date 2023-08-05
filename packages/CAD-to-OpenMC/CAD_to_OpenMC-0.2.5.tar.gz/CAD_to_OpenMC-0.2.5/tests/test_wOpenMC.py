import pytest
from tests.testRun import *
import sys

class TestSphereOpenMC(TestRun):
  def __init__(self):
    super().__init__()
  
  def run(self):
    assert True

  def _build_geometry(self):
    du=openmc.DAGMCUniverse('dagmc.h5m')
    br=du.bounding_region(boundary_type='transmission')
    inner=openmc.Cell(region=br, fill=du)
    bndr=openmc.Sphere(r=10,boundary_type='vacuum')
    outer=openmc.Cell(region=~br & -bndr)
    root=openmc.Universe()
    root.add_cells([inner,outer])
    return openmc.Geometry(root)

  def _build_settings(self):
    s=openmc.Settings(particles=1000, inactive=0, batches=3)
    s.run_mode='eigenvalue'
    src=openmc.Source(space=openmc.Point(), energy=openmc.stats.Discrete([14.1e6],[1.0]) )
    s.source=src
    return s

  def _run_openmc(self):
    mod=openmc.Model(geometry=self._build_geometry(), settings=self._build_settings())
    mod.run()
      
  

@pytest.mark.skipif('openmc' not in sys.modules, reason='OpenMC is not available')
def testSphereOpenMC():
  t = TestSphereOpenMC()
  t.run()
