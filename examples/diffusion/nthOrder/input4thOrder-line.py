#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 7/5/07 {6:03:30 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

"""
   >>> eq.solve(var,
   ...          boundaryConditions = BCs,
   ...          solver = solver)

   Using the Pysparse solvers, the answer is totally inaccurate. This is due to
   the 4th order term having a high matrix condition number. In this particular
   example, multigrid preconditioners such as those provided by Trilinos allow
   a more accurate solution.

   >>> print var.allclose(mesh.getCellCenters()[0], atol = tolerance)
   1

"""
__docformat__ = 'restructuredtext'

from fipy import *

Lx = 1.
nx = 100000
dx = Lx / nx

mesh = Grid1D(dx = dx, nx = nx)

var = CellVariable(mesh = mesh)

eq = ImplicitDiffusionTerm((1.0, 1.0))

BCs = (NthOrderBoundaryCondition(mesh.getFacesLeft(), 0., 0),
       NthOrderBoundaryCondition(mesh.getFacesRight(), Lx, 0),
       NthOrderBoundaryCondition(mesh.getFacesLeft(), 0., 2),
       NthOrderBoundaryCondition(mesh.getFacesRight(), 0., 2))

if solverSuite() == 'Trilinos':
    solver = LinearPCGSolver(tolerance=1e-30)
    tolerance = 1e-2
else:
    solver = LinearLUSolver(iterations=10)
    tolerance = 10

if __name__ == '__main__':
    eq.solve(var,
             boundaryConditions = BCs,
             solver = solver)
    
    viewer = viewers.make(var)
    viewer.plot()

    print var.allclose(mesh.getCellCenters()[0], atol = tolerance)
    raw_input("finished")
