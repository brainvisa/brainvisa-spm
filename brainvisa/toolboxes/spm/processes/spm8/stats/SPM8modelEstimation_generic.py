# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
from __future__ import absolute_import
from brainvisa.processes import *
from soma.spm.spm8.stats.model_estimation import ModelEstimationClassical, ModelEstimationBayesianSecondLevel, ModelEstimationBayesianFirstLevel
from soma.spm.spm8.stats.model_estimation.analysis_space import AnalysisSpaceVolume, AnalysisSpaceSlices, AnalysisSpaceClusters
from soma.spm.spm8.stats.model_estimation.simple_contrast import SimpleContrast
from soma.spm.spm_launcher import SPM8, SPM8Standalone
from six.moves import range
#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  try:
    spm = SPM8Standalone(configuration.SPM.spm8_standalone_command,
                         configuration.SPM.spm8_standalone_mcr_path,
                         configuration.SPM.spm8_standalone_path)
  except:
    spm = SPM8(configuration.SPM.spm8_path,
               configuration.matlab.executable,
               configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 0
name = 'spm8 - Estimation Model - generic'

signature = Signature(
  'basic_model_mat_file', ReadDiskItem('Matlab SPM file', 'Matlab file'),
  'method', Choice('Classical', 'Bayesian 1st-level', 'Bayesian 2nd-level'),

  #analysis Space
  'analysis_space', Choice('Volume', 'Slices', 'Clusters'),
  'block_type', Choice('Slices', 'Subvolumes'),
  #analysis Space : Slices
  'slice_number', ListOf(Integer()),
  #analysis Space : Clusters
  'cluster_mask', ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'] ),

  'signal_priors', Choice('UGL', 'GMRF', 'LORETA', 'WGL', 'Global', 'Uninformative'),
  'AR_model_order', ListOf(Integer()),
  #Noise priors
  'noise_priors', Choice('UGL', 'GMRF', 'LORETA', 'Tissue-type', 'Robust'),
  'tissue_type', ReadDiskItem( '4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'] ),

  'log_evidence_map', Boolean(),
  #ANOVA
  'first_level_anova', Boolean(),
  'second_level_anova', Boolean(),
  #Simple Contrasts
  'simple_contrast_number', Integer(),
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
)

def initialization( self ):
  self.simple_contrast_number = 0
  self.simple_contrast_current_number = 0

  self.addLink(None, 'method', self.updateSignatureByMethodUsed)
  self.addLink(None, 'analysis_space', self.updateSignatureByAnalysisSpace)
  self.addLink(None, 'noise_priors', self.updateTissueTypeSignature)
  self.addLink(None, 'simple_contrast_number', self.updateSignatureAboutSimpleContrastNumber)

  self.addLink("batch_location", "basic_model_mat_file", self.updateBatchPath)

  self.analysis_space = 'Volume'
  self.AR_model_order = [3]
  self.signal_priors = 'UGL'
  self.log_evidence_map = False
  self.first_level_anova = False
  self.second_level_anova = True

def updateSignatureByMethodUsed(self, proc):
  if self.method == 'Bayesian 1st-level':
    self.setEnable("analysis_space",
                   "block_type",
                   "slice_number",
                   "cluster_mask",
                   "signal_priors",
                   "AR_model_order",
                   "noise_priors",
                   "tissue_type",
                   "log_evidence_map",
                   "first_level_anova",
                   "second_level_anova",
                   "simple_contrast_number",
                   userLevel=1)
  else:
    self.setDisable("analysis_space",
                    "block_type",
                    "slice_number",
                    "cluster_mask",
                    "signal_priors",
                    "AR_model_order",
                    "noise_priors",
                    "tissue_type",
                    "log_evidence_map",
                    "first_level_anova",
                    "second_level_anova",
                    "simple_contrast_number")


  for simple_contrast_index in range(self.simple_contrast_number):
    if self.method == 'Bayesian 1st-level':
      self.setEnable("simple_contrast_%s_name" %simple_contrast_index,
                     "simple_contrast_%s_vector" %simple_contrast_index,
                     userLevel=1)
    else:
      self.setDisable("simple_contrast_%s_name" %simple_contrast_index,
                      "simple_contrast_%s_vector" %simple_contrast_index)

  self.changeSignature(self.signature)
  if self.method == 'Bayesian 1st-level':
    self.updateSignatureByAnalysisSpace(proc)
    self.updateTissueTypeSignature(proc)

def updateSignatureByAnalysisSpace(self, proc):
  if self.analysis_space == 'Volume':
    self.setDisable("slice_number", "cluster_mask")
  elif self.analysis_space == 'Slices':
    self.setEnable("slice_number", userLevel=1)
    self.setDisable("cluster_mask")
  else:
    self.setEnable("cluster_mask", userLevel=1)
    self.setDisable("slice_number")
  self.changeSignature(self.signature)

def updateTissueTypeSignature(self, proc):
  if self.noise_priors == "Tissue-type":
    self.setEnable("tissue_type", userLevel=1)
  else:
    self.setDisable("tissue_type")
  self.changeSignature(self.signature)

def updateSignatureAboutSimpleContrastNumber(self, proc):
  if self.simple_contrast_number < self.simple_contrast_current_number:
    for simple_contrast_index in range(self.simple_contrast_number,self.simple_contrast_current_number):
      self.removeSimpleContrastInSignature(simple_contrast_index)
  else:
    for simple_contrast_index in range(self.simple_contrast_current_number,self.simple_contrast_number):
      self.addSimpleContrastInSignature(simple_contrast_index)
  self.simple_contrast_current_number = self.simple_contrast_number
  self.changeSignature(self.signature)

def removeSimpleContrastInSignature(self, simple_contrast_index):
  del self.signature["simple_contrast_%s_name" %simple_contrast_index]
  del self.signature["simple_contrast_%s_vector" %simple_contrast_index]

def addSimpleContrastInSignature(self, simple_contrast_index):
  self.signature["simple_contrast_%s_name" %simple_contrast_index] = String()
  self.signature["simple_contrast_%s_vector" %simple_contrast_index] = ListOf(Float())

def updateBatchPath(self, proc):
  if self.basic_model_mat_file is not None:
    directory_path = os.path.dirname(self.basic_model_mat_file.fullPath())
    return os.path.join(directory_path, 'spm8_model_estimation_job.m')

def execution( self, context ):
  if self.method == 'Classical':
    classical_estimation = ModelEstimationClassical()
    classical_estimation.setMatlabFilePath(str(self.basic_model_mat_file.fullPath()))

    spm = validation()
    spm.addModuleToExecutionQueue(classical_estimation)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
    return

  elif self.method == 'Bayesian 2nd-level':
    bayesian_second_level_estimation = ModelEstimationBayesianSecondLevel()
    bayesian_second_level_estimation.setMatlabFilePath(str(self.basic_model_mat_file.fullPath()))

    spm = validation()
    spm.addModuleToExecutionQueue(bayesian_second_level_estimation)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
    return

  else:
    if self.analysis_space == 'Volume':
      analysis_space = AnalysisSpaceVolume()
    elif self.analysis_space == 'Slices':
      analysis_space = AnalysisSpaceSlices()
      analysis_space.setSliceNumberList(self.slice_number)
    else:
      analysis_space = AnalysisSpaceClusters()
      analysis_space.setClusterMask(self.cluster_mask.fullPath())

    bayesian_first_level_estimation = ModelEstimationBayesianFirstLevel()
    bayesian_first_level_estimation.setMatlabFilePath(str(self.basic_model_mat_file.fullPath()))
    bayesian_first_level_estimation.setAnalysisSpace(analysis_space)

    if self.signal_priors == "UGL":
      bayesian_first_level_estimation.setSignalPriorsToUGL()
    elif self.signal_priors == "GMRF":
      bayesian_first_level_estimation.setSignalPriorsToGMRF()
    elif self.signal_priors == "LORETA":
      bayesian_first_level_estimation.setSignalPriorsToLORETA()
    elif self.signal_priors == "UGL":
      bayesian_first_level_estimation.setSignalPriorsToWGL()
    elif self.signal_priors == "UGL":
      bayesian_first_level_estimation.setSignalPriorsToGlobal()
    elif self.signal_priors == "UGL":
      bayesian_first_level_estimation.setSignalPriorsToUninformative()
    else:
      raise ValueError("Unvalid signal_priors")
    bayesian_first_level_estimation.setSignalPriors(self.signal_priors)
    bayesian_first_level_estimation.setARModelOrderVector(self.AR_model_order)
    '', '', '', '', ''
    if self.signal_priors == "UGL":
      bayesian_first_level_estimation.setNoisePriorsToUGL()
    elif self.signal_priors == "GMRF":
      bayesian_first_level_estimation.setNoisePriorsToGMRF()
    elif self.signal_priors == "LORETA":
      bayesian_first_level_estimation.setNoisePriorsToLORETA()
    elif self.signal_priors == "Tissue-type":
      bayesian_first_level_estimation.setNoisePriorsToTissueType()
      bayesian_first_level_estimation.setTissueTypePath(self.tissue_type.fullPath())
    elif self.signal_priors == "Robust":
      bayesian_first_level_estimation.setNoisePriorsToRobust()
    else:
      raise ValueError("Unvalid signal_priors")

    if self.log_evidence_map:
      bayesian_first_level_estimation.saveLogEvidenceMap()
    else:
      bayesian_first_level_estimation.discardLogEvidenceMap()

    if self.first_level_anova:
      bayesian_first_level_estimation.enableFirstLevelANOVA()
    else:
      bayesian_first_level_estimation.disableFirstLevelANOVA()

    if self.second_level_anova:
      bayesian_first_level_estimation.enableSecondLevelANOVA()
    else:
      bayesian_first_level_estimation.disableSecondLevelANOVA()

    simple_contrast_list = []
    for simple_contrast_index in range(self.simple_contrast_number):
      simple_contrast = SimpleContrast()
      simple_contrast.setName(eval("self.simple_contrast_%s_name" %simple_contrast_index))
      simple_contrast.setVector(eval("self.simple_contrast_%s_name" %simple_contrast_index))
      simple_contrast_list.append(simple_contrast)

    bayesian_first_level_estimation.setSimpleContrastList(simple_contrast_list)
    bayesian_first_level_estimation.start(configuration, self.batch_location.fullPath())

    spm = validation()
    spm.addModuleToExecutionQueue(bayesian_first_level_estimation)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)


