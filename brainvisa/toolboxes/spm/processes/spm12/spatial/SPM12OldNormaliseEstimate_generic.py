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
from brainvisa.processes import *
from soma.spm.spm12.spatial.old_normalise import Estimate
from soma.spm.spm12.spatial.old_normalise.subject import SubjectToEstimate
from soma.spm.spm12.spatial.old_normalise.estimation_options import EstimationOptions
from soma.spm.spm_launcher import SPM12, SPM12Standalone

#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  try:
    spm = SPM12Standalone(configuration.SPM.spm12_standalone_command,
                          configuration.SPM.spm12_standalone_mcr_path,
                          configuration.SPM.spm12_standalone_path)
  except:
    spm = SPM12(configuration.SPM.spm12_path,
                configuration.matlab.executable,
                configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 1
name = 'spm12 - Old normalise: Estimate only - generic'

subject_section = "subject options"
estimation_section = "Estimation options"

signature = Signature(
  "source", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'], section=subject_section),
  "source_weighting", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'], section=subject_section),

  "template", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'], section=estimation_section),
  "template_weighting", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'], section=estimation_section),
  "source_smoothing", Float(section=estimation_section),
  "template_smoothing", Float(section=estimation_section),
  "affine_regularisation", Choice("ICBM space template",
                                  "Average sized template",
                                  "No regularisation", section=estimation_section),
  "frequency_cutoff", Float(section=estimation_section),
  "iterations", Integer(section=estimation_section),
  "regularisation", Float(section=estimation_section),

  "sn_mat", WriteDiskItem( 'Matlab SPM script', 'Matlab file', section='SPM outputs' ),
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default outputs' ),
)
def initialization(self):
  self.setOptional("source_weighting", "template_weighting", "sn_mat")

  self.addLink("batch_location", "source", self.updateBatchPath)

  #SPM default initialisation
  self.source_smoothing = 8
  self.template_smoothing = 0
  self.affine_regularisation = "ICBM space template"
  self.frequency_cutoff = 25
  self.iterations = 16
  self.regularisation = 1

def checkIfNotEmpty(self, proc):
  if self.filename_prefix in [None, '']:
    self.filename_prefix = 'w'
  else:
    pass

def updateBatchPath(self, proc):
  if self.source is not None:
    directory_path = os.path.dirname(self.source.fullPath())
    return os.path.join(directory_path, 'spm8_normalise_estimate_job.m')

def execution( self, context ):
  estimate = Estimate()

  subject = SubjectToEstimate()
  subject.setSourceImage(self.source.fullPath())

  if self.source_weighting is not None:
    subject.setSourceWeightingImage(self.source_weighting.fullPath())

  if self.sn_mat is not None:
    subject.setSnMatOutputPath(self.sn_mat.fullPath())
  else:
    pass#SPM default outputs

  estimate.appendSubject(subject)

  estimation_options = EstimationOptions()
  estimation_options.setTemplateImage(self.template.fullPath())
  if self.template_weighting is not None:
    estimation_options.setTemplateWeightingImage(self.template_weighting.fullPath())
  estimation_options.setSourceImageSmoothing(self.source_smoothing)
  estimation_options.setTemplateImageSmoothing(self.template_smoothing)
  if self.affine_regularisation == "ICBM space template":
    estimation_options.setAffineRegularisationToICBMSpaceTemplate()
  elif self.affine_regularisation == "Average sized template":
    estimation_options.setAffineRegularisationToAverageSizedTemplate()
  elif self.affine_regularisation == "No regularisation":
    estimation_options.unsetAffineRegularisation()
  else:
    raise ValueError("Unvalid choice for affine_regularisation")

  estimation_options.setNonLinearFrequencyCutOff(self.frequency_cutoff)
  estimation_options.setNonLinearIterations(self.iterations)
  estimation_options.setNonLinearRegularisation(self.regularisation)

  estimate.replaceEstimateOptions(estimation_options)

  spm = validation()
  spm.addModuleToExecutionQueue(estimate)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
