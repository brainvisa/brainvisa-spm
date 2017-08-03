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
from soma.spm.spm12.stats.contrast_manager import ContrastManager
from soma.spm.spm12.stats.contrast_manager.tcontrast import TContrast
from soma.spm.spm12.stats.contrast_manager.fcontrast import FContrast, FContrastVector
from soma.spm.spm12.stats.contrast_manager.tcontrast_condsessbased import TContrastCondSessBased#useless but exists

import numpy
import os
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
name = 'spm12 - Contrast Manager - generic'


signature = Signature(
  'contrast_mat_file', ReadDiskItem( 'Matlab SPM file', 'Matlab file' ),
  'T_contrast_number', Integer(),
  'F_contrast_number', Integer(),
#  'T_contrast_cond_sess_based_number', Integer(),
  'delete_existing_contrast', Boolean(),
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
  'start_now', Boolean(),
)

def initialization( self ):
  self.setOptional("contrast_mat_file")  # because if spm pipeline in batch
  self.addLink(None, 'T_contrast_number', self.updateSignatureAboutTContrast)
  self.addLink(None, 'F_contrast_number', self.updateSignatureAboutFContrast)

  self.addLink("batch_location", "contrast_mat_file", self.updateBatchPath)

  #----------------------------------------------------------------------------
  self.T_contrast_current_number = 0
  self.T_contrast_number = 1
  self.T_contrast_0_name = 'contrast'
  self.T_contrast_0_weights_vector = [1,-1]
  self.T_contrast_0_replicate = 'Do not replicate'
  self.F_contrast_current_number = 0
  self.F_contrast_number = 0
  #self.T_contrast_cond_sess_based_current_number = 0#Not implemented yet
  #self.T_contrast_cond_sess_based_number = 0

  #SPM default initialisation
  self.delete_existing_contrast = False
#==============================================================================
# T Contrast Dynamic Signature
#==============================================================================
def updateSignatureAboutTContrast(self, proc):
  if self.T_contrast_number < self.T_contrast_current_number:
    for T_contrast_index in range(self.T_contrast_number,self.T_contrast_current_number):
      self.removeTContrastInSignature(T_contrast_index)
  else:
    for T_contrast_index in range(self.T_contrast_current_number,self.T_contrast_number):
      self.addTContrastInSignature(T_contrast_index)
  self.T_contrast_current_number = self.T_contrast_number
  self.changeSignature(self.signature)

def removeTContrastInSignature(self, T_contrast_index):
  del self.signature['T_contrast_' + str(T_contrast_index) + '_name']
  del self.signature['T_contrast_' + str(T_contrast_index) + '_weights_vector']
  del self.signature['T_contrast_' + str(T_contrast_index) + '_replicate']

def addTContrastInSignature(self, T_contrast_index):
  self.signature['T_contrast_' + str(T_contrast_index) + '_name'] = String()
  self.signature['T_contrast_' + str(T_contrast_index) + '_weights_vector'] = ListOf(Float())
  self.signature['T_contrast_' + str(T_contrast_index) + '_replicate'] = Choice('Do not replicate',
                                                                                'Create per session',
                                                                                'Replicate',
                                                                                'Replicate and Scale and Create per session',
                                                                                'Replicate and Scale',
                                                                                'Replicate and Create per session')
#==============================================================================
# F Contrast Dynamic Signature
#==============================================================================
def updateSignatureAboutFContrast(self, proc):
  if self.F_contrast_number < self.F_contrast_current_number:
    for F_contrast_index in range(self.F_contrast_number,self.F_contrast_current_number):
      self.removeFContrastInSignature(F_contrast_index)
  else:
    for F_contrast_index in range(self.F_contrast_current_number,self.F_contrast_number):
      self.addFContrastInSignature(F_contrast_index)
  self.F_contrast_current_number = self.F_contrast_number
  self.changeSignature(self.signature)

def removeFContrastInSignature(self, F_contrast_index):
  del self.signature['F_contrast_' + str(F_contrast_index) + '_name']
  del self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix_row']
  del self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix_column']
  del self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix']
  del self.signature['F_contrast_' + str(F_contrast_index) + '_replicate']

def addFContrastInSignature(self, F_contrast_index):
  self.signature['F_contrast_' + str(F_contrast_index) + '_name'] = String()
  self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix_row'] = Integer()
  self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix_column'] = Integer()
  self.signature['F_contrast_' + str(F_contrast_index) + '_weights_matrix'] = ListOf(Float())
  self.signature['F_contrast_' + str(F_contrast_index) + '_replicate'] = Choice('Do not replicate',
                                                                                'Replicate average and Create per session',
                                                                                'Create per session',
                                                                                'Replicate no averaging',
                                                                                'Replicate average'
                                                                                )

def updateBatchPath(self, proc):
  if self.contrast_mat_file is not None:
    directory_path = os.path.dirname(self.contrast_mat_file.fullPath())
    return os.path.join(directory_path, 'spm12_contrast_manager_job.m')
#==============================================================================
# execution
#==============================================================================
def execution(self, context):
  contrast_manager = ContrastManager()
  contrast_manager.setMatlabFilePath(str(self.contrast_mat_file.fullPath()))
  if self.delete_existing_contrast:
    contrast_manager.deleteExistingContrast()
  else:
    contrast_manager.keepExistingContrast()

  for T_contrast_index in range(self.T_contrast_current_number):
    T_contrast = TContrast()
    T_contrast.setName(eval('self.T_contrast_' + str(T_contrast_index) + '_name'))
    T_contrast.setVector(eval('self.T_contrast_' + str(T_contrast_index) + '_weights_vector'))
    T_contrast.setReplicateOverSessions(eval('self.T_contrast_' + str(T_contrast_index) + '_replicate'))
    contrast_manager.appendContrast(T_contrast)

  for F_contrast_index in range(self.F_contrast_current_number):
    F_contrast = FContrast()
    F_contrast.setName(eval('self.F_contrast_' + str(F_contrast_index) + '_name'))
    F_contrast_matrix = self.createFContrastMatrix(F_contrast_index)
    F_contrast.setFContrastWeightsMatrix(F_contrast_matrix)
    F_contrast.setReplicateOverSessions(eval('self.F_contrast_' + str(F_contrast_index) + '_replicate'))
    contrast_manager.appendContrast(F_contrast)

  spm = validation()
  spm.addModuleToExecutionQueue(contrast_manager)
  if self.start_now:
      spm.setSPMScriptPath(self.batch_location.fullPath())
      output = spm.run()
      context.log(name, html=output)

def createFContrastMatrix(self, F_contrast_index):
  f_contrast_vector = FContrastVector()
  row_count = eval('self.F_contrast_' + str(F_contrast_index) + '_weights_matrix_row')
  column_count = eval('self.F_contrast_' + str(F_contrast_index) + '_weights_matrix_column')
  f_contrast_list = eval('self.F_contrast_' + str(F_contrast_index) + '_weights_matrix')
  f_contrast_vector.setFContrastVector(numpy.reshape(f_contrast_list, (row_count,column_count)))
  return f_contrast_vector




