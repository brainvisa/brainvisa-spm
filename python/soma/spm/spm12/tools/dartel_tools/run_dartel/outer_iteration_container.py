# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm12.tools.dartel_tools.run_dartel.outer_iteration import OuterIteration
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.outer_iteration_container import OuterIterationContainer as OuterIterationContainer_virtual

from soma.spm.spm_container import SPMContainer

class OuterIterationContainer(OuterIterationContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, OuterIteration)

    first_outer_iteration = OuterIteration()
    first_outer_iteration.setInnerIterationsNumber(3)
    first_outer_iteration.setRegParams([4, 2, 1e-06])
    first_outer_iteration.setTimeSteps(1)
    first_outer_iteration.setSmoothingParameter(16)
    self.append(first_outer_iteration)

    second_outer_iteration = OuterIteration()
    second_outer_iteration.setInnerIterationsNumber(3)
    second_outer_iteration.setRegParams([2, 1, 1e-06])
    second_outer_iteration.setTimeSteps(1)
    second_outer_iteration.setSmoothingParameter(8)
    self.append(second_outer_iteration)

    third_outer_iteration = OuterIteration()
    third_outer_iteration.setInnerIterationsNumber(3)
    third_outer_iteration.setRegParams([1, 0.5, 1e-06])
    third_outer_iteration.setTimeSteps(2)
    third_outer_iteration.setSmoothingParameter(4)
    self.append(third_outer_iteration)

    fourth_outer_iteration = OuterIteration()
    fourth_outer_iteration.setInnerIterationsNumber(3)
    fourth_outer_iteration.setRegParams([0.5, 0.25, 1e-06])
    fourth_outer_iteration.setTimeSteps(4)
    fourth_outer_iteration.setSmoothingParameter(2)
    self.append(fourth_outer_iteration)

    fifth_outer_iteration = OuterIteration()
    fifth_outer_iteration.setInnerIterationsNumber(3)
    fifth_outer_iteration.setRegParams([0.25, 0.125, 1e-06])
    fifth_outer_iteration.setTimeSteps(16)
    fifth_outer_iteration.setSmoothingParameter(1)
    self.append(fifth_outer_iteration)

    sixth_outer_iteration = OuterIteration()
    sixth_outer_iteration.setInnerIterationsNumber(3)
    sixth_outer_iteration.setRegParams([0.25, 0.125, 1e-06])
    sixth_outer_iteration.setTimeSteps(64)
    sixth_outer_iteration.setSmoothingParameter(0.5)
    self.append(sixth_outer_iteration)
