# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
import numbers

class OptimisationSettings():
  """
  Settings  for  the  optimisation.    If  you  are  unsure  about them, then leave them at the default values.  Optimisation is by repeating a
  number  of  Levenberg-Marquardt  iterations,  in  which  the  equations  are  solved  using  a  full  multi-grid  (FMG)  scheme.  FMG and
  Levenberg-Marquardt are both described in Numerical Recipes (2nd edition).
  """
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setLMRegularisation(self, LM_regularisation):
    """
    Levenberg-Marquardt  regularisation.    Larger  values increase the the stability of
    the  optimisation,  but  slow  it down.  A value of zero results in a Gauss-Newton
    strategy, but this is not recommended as it may result in instabilities in the FMG.
    """
    self.LM_regularisation = LM_regularisation
    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setCycles(self, cycles):
    """
    Number  of  cycles used by the full multi-grid matrix solver. More cycles result in
    higher  accuracy,  but  slow  down the algorithm. See Numerical Recipes for more
    information on multi-grid methods.
    """
    if cycles in [1, 2, 3, 4, 5, 6, 7, 8]:
      self.cycles = cycles
    else:
      raise ValueError("Unvalid cycles")
    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setIterations(self, iterations):
    """
    Number   of   relaxation   iterations  performed  in  each  multi-grid  cycle.  More
    iterations  are  needed  if  using  ``bending  energy''  regularisation,  because the
    relaxation  scheme  only  runs  very  slowly.  See  the  chapter  on  solving partial
    differential  equations in Numerical Recipes for more information about relaxation
    methods.
    """
    if iterations in [1, 2, 3, 4, 5, 6, 7, 8]:
      self.iterations = iterations
    else:
      raise ValueError("Unvalid cycles")
    
  def getStringListForBatch(self):
    if not None in [self.LM_regularisation, self.cycles, self.iterations]:
      batch_list = []
      batch_list.append("optim.lmreg =  " + str(self.LM_regularisation) + ";")
      batch_list.append("optim.cyc =  " + str(self.cycles) + ';')
      batch_list.append("optim.its = " + str(self.iterations) + ';')
      return batch_list  
    else:
      raise ValueError('At least one OptimisationSettings parameter missed')
    