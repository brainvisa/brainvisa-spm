# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design import FactorialDesign as FactorialDesign_virtual
from soma.spm.virtual_spm.stats.factorial_design import OneSampleTTest as OneSampleTTest_virtual
from soma.spm.virtual_spm.stats.factorial_design import TwoSampleTTest as TwoSampleTTest_virtual
from soma.spm.virtual_spm.stats.factorial_design import PairedTTest as PairedTTest_virtual
from soma.spm.spm_main_module import SPM8MainModule

from soma.spm.spm8.stats.factorial_design.directory import Directory
from soma.spm.spm8.stats.factorial_design.covariate_container import CovariateContainer
from soma.spm.spm8.stats.factorial_design.masking import Masking
from soma.spm.spm8.stats.factorial_design.global_calculation import GlobalCalculation
from soma.spm.spm8.stats.factorial_design.global_normalisation import GlobalNormalisation
from soma.spm.spm8.stats.factorial_design.one_sample_ttest_design import OneSampleTTestDesign
from soma.spm.spm8.stats.factorial_design.two_sample_ttest_design import TwoSampleTTestDesign
from soma.spm.spm8.stats.factorial_design.paired_ttest_design import PairedTTestDesign

#==============================================================================
class FactorialDesign(FactorialDesign_virtual):
  def __init__(self):
    self.directory = Directory()
    self.design = None
    self.covariate_container = CovariateContainer()
    self.masking = Masking()
    self.global_calculation = GlobalCalculation()
    self.global_normalisation = GlobalNormalisation()
#==============================================================================
class OneSampleTTest(FactorialDesign, OneSampleTTest_virtual, SPM8MainModule):
  def __init__(self):
    FactorialDesign.__init__(self)#TODO : maybe move it here ?
    self.design = OneSampleTTestDesign()
#==============================================================================
class TwoSampleTTest(FactorialDesign, TwoSampleTTest_virtual, SPM8MainModule):
  def __init__(self):
    FactorialDesign.__init__(self)#TODO : maybe move it here ?
    self.design = TwoSampleTTestDesign()

#==============================================================================
class PairedTTest(FactorialDesign, PairedTTest_virtual, SPM8MainModule):
  def __init__(self):
    FactorialDesign.__init__(self)#TODO : maybe move it here ?
    self.design = PairedTTestDesign()

