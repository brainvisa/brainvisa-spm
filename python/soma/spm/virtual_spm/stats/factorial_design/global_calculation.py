# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class GlobalCalculation():
  """
  This option is only used for PET data.
  There  are  three  methods  for  estimating global effects (1) Omit (assumming no
  other  options  requiring the global value chosen) (2) User defined (enter your own
  vector  of  global  values)  (3)  Mean:  SPM  standard mean voxel value (within per
  image fullmean/8 mask)
  """
   
  def setGlobalCalculationMethodToOmit(self):
    self.method = "Omit"
    
  def setGlobalCalculationMethodToUser(self):
    self.method = "User"
    
  def setGlobalCalculationMethodToMean(self):
    self.method = "Mean"

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setValuesForUserMethod(self, values_list):
    self.user_global_values_list = values_list
    
  def getStringListForBatch( self ):
    if self.method == 'Omit':
      batch_list = [ "globalc.g_omit = 1;"]
    elif self.method == 'User':
      value_str = [ str( val ) for val in self.user_global_values_list ]
      user_global_values_str = '\n'.join( value_str )
      batch_list = ["globalc.g_user.global_uval = [%s];" % user_global_values_str]
    elif self.method == 'Mean':
      batch_list = ["globalc.g_mean = 1;"]
    return batch_list