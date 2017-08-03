 # -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
import numbers

class WarpingOptions():
  """
  There are a couple of user-customisable warping options.
  """
  @checkIfArgumentTypeIsAllowed(int, argument_index=1)
  def setIterations(self, iteration):
    """
    Number of iterations for the warping.
    """
    self.iteration = iteration
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, argument_index=1)
  def setWarpingRegularisation(self, warping_regularisation):
    """
    There  is  a  tradeoff  between  the  smoothness  of the estimated warps, and the
    difference  between  the registered images.  Higher values mean smoother warps,
    at the expense of a lower mean squared difference between the images.
    """
    self.warping_regularisation = warping_regularisation
    
  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("warp_opts.nits = %i;" % self.iteration)
    batch_list.append("warp_opts.reg = %g;" % self.warping_regularisation)
    return batch_list