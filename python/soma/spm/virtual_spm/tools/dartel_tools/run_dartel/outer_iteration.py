# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class OuterIteration(object):
  """
  Different parameters can be specified for each outer iteration. Each of them warps the images to the template, and then regenerates the
  template  from  the  average  of the warped images. Multiple outer iterations should be used for more accurate results, beginning with a
  more coarse registration (more regularisation) then ending with the more detailed registration (less regularisation).
  """
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setInnerIterationsNumber(self, inner_iterations):
    """
    The  number  of  Gauss-Newton  iterations  to be done within this outer iteration.
    After  this,  new average(s) are created, which the individual images are warped to
    match.
    """
    if inner_iterations in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
      self.inner_iterations = inner_iterations
    else:
      raise ValueError("Unvalid Inner iterations")
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setRegParams(self, reg_params_list):
    """
    For linear elasticity, the parameters are mu, lambda and id. For membrane energy,
    the  parameters  are  lambda,  unused  and  id.id is a term for penalising absolute
    displacements,   and   should   therefore   be   small.    For  bending  energy,  the
    parameters    are    lambda,    id1    and    id2,    and   the   regularisation   is   by
    (-lambda*Laplacian + id1)^2 + id2.
    """
    if len(reg_params_list) == 3:
      self.reg_params = reg_params_list
    else:
      raise ValueError("Unvalid Reg params")
    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setTimeSteps(self, time_steps):
    """
    The  number  of  time points used for solving the partial differential equations.  A
    single  time  point  would  be  equivalent  to  a  small deformation model. Smaller
    values  allow  faster  computations,  but  are  less  accurate  in  terms  of inverse
    consistency  and  may  result  in the one-to-one mapping breaking down.  Earlier
    iteration  could  use  fewer  time  points,  but  later ones should use about 64 (or
    fewer if the deformations are very smooth).
    """
    if time_steps in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
      #WARNING : For SPM batch, it is the index in this list to write! (but i don't know why SPM do this)
      self.time_steps = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512].index(time_steps)
    else:
      raise ValueError("Unvalid time steps")
    
  def setSmoothingParameter(self, smoothing_parameter):
    """
    A  LogOdds  parameterisation  of  the  template  is  smoothed  using a multi-grid
    scheme.  The amount of smoothing is determined by this parameter.
    """
    if smoothing_parameter in [0.5, 1, 2, 4, 8, 16, 32]:
      self.smoothing_parameter = smoothing_parameter
    elif smoothing_parameter is None:
      self.smoothing_parameter = 0
    else:
      raise ValueError("Unvalid smoothing parameters")
    
  def getStringListForBatch(self):
    if not None in [self.inner_iterations, self.reg_params, self.time_steps, self.smoothing_parameter]:
      batch_list = []
      batch_list.append("its = " + str(self.inner_iterations) + ';' )
      batch_list.append("rparam = " + convertlistToSPMString(self.reg_params) + ';')
      batch_list.append("K = " + str(self.time_steps) + ';')
      batch_list.append("slam = " + str(self.smoothing_parameter) + ';')
      return batch_list  
    else:
      raise ValueError('At least one OuterIteration parameter missed')
    