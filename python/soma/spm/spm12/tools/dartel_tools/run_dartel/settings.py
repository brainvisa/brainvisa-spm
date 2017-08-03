# -*- coding: utf-8 -*-
from soma.spm.spm12.tools.dartel_tools.run_dartel.outer_iteration_container import OuterIterationContainer
from soma.spm.spm12.tools.dartel_tools.run_dartel.optimisation_settings import OptimisationSettings
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.settings import Settings as Settings_virtual

class Settings(Settings_virtual):
  def __init__(self):
    self.template_basename = 'Template'
    self.regularisation_form = 0
    self.outer_iteration_container = OuterIterationContainer()
    self.optimisation_settings = OptimisationSettings()
  
