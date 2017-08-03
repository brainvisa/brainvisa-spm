# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.optimisation_settings import OptimisationSettings

from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class Settings():
  """
  Various settings for the optimisation. The default values should work reasonably well for aligning tissue class images together.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setTemplateBasename(self, template_basename):
    """
    Enter  the  base  for  the  template  name.    Templates  generated  at  each outer
    iteration  of  the procedure will be basename_1.nii, basename_2.nii etc.  If empty,
    then  no  template  will be saved. Similarly, the estimated flow-fields will have the
    basename appended to them.
    """
    self.template_basename = template_basename

  def setRegularisationFormToLinearElasticEnergy(self):
    """
    The  registration  is  penalised  by  some  ``energy'' term.  Here, the form of this
    energy  term  is specified. Three different forms of regularisation can currently be
    used.
    """
    self.regularisation_form = 0

  def setRegularisationFormToMembraneEnergy(self):
    """
    The  registration  is  penalised  by  some  ``energy'' term.  Here, the form of this
    energy  term  is specified. Three different forms of regularisation can currently be
    used.
    """
    self.regularisation_form = 1

  def setRegularisationFormToBendingEnergy(self):
    """
    The  registration  is  penalised  by  some  ``energy'' term.  Here, the form of this
    energy  term  is specified. Three different forms of regularisation can currently be
    used.
    """
    self.regularisation_form = 2

  def clearOuterIterationContainer(self):
    self.outer_iteration_container.clear()

  def appendOuterIteration(self, outer_iteration):
    self.outer_iteration_container.append(outer_iteration)

  @checkIfArgumentTypeIsAllowed(OptimisationSettings, 1)
  def setOptimisationSettings(self, optimisation_settings):
    self.optimisation_settings = optimisation_settings

  def getOuterIterationNumber(self):
    return len(self.outer_iteration_container)

  def getTemplateBasename(self):
    return self.template_basename

  def getStringListForBatch( self ):
    if not None in [self.outer_iteration_container, self.optimisation_settings]:
      batch_list = []
      batch_list.append("settings.template = '%s';" % self.template_basename)
      batch_list.append("settings.rform = %i;" % self.regularisation_form)
      batch_list.extend(addBatchKeyWordInEachItem("settings", self.outer_iteration_container.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("settings", self.optimisation_settings.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('outer_iteration_container and/or optimisation_settings not found')



