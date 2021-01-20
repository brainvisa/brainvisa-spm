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

configuration = Application().configuration

userLevel = 0
name = "import t1mri templates"

signature = Signature(
  'template_to_import', ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
  'template_type', Choice('TPM HDW DARTEL template', 'TPM template'),
  'template_TPM_HDW_imported', WriteDiskItem('TPM HDW DARTEL template', 'NIFTI-1 image'),
  'template_TPM_imported', WriteDiskItem('TPM template', 'NIFTI-1 image'),
)

def initialization(self):
  self.signature["template_to_import"].databaseUserLevel = configuration.brainvisa.userLevel + 1
  self.signature["template_TPM_HDW_imported"].browseUserLevel = configuration.brainvisa.userLevel + 1
  self.signature["template_TPM_imported"].browseUserLevel = configuration.brainvisa.userLevel + 1
  self.addLink(None, "template_type", self.updateSignatureAboutTemplate)
  
def updateSignatureAboutTemplate(self, proc):
  if self.template_type == "TPM HDW DARTEL template":
    self.setEnable("template_TPM_HDW_imported")
    self.setDisable("template_TPM_imported")
  elif self.template_type == "TPM template":
    self.setEnable("template_TPM_imported")
    self.setDisable("template_TPM_HDW_imported")
  else:
    raise ValueError("Unvalid template_type")
  self.changeSignature(self.signature)
  
def execution(self, context):
  if self.template_type == "TPM HDW DARTEL template":
    shutil.copy(self.template_to_import.fullPath(), self.template_TPM_HDW_imported.fullPath())
  elif self.template_type == "TPM template":
    shutil.copy(self.template_to_import.fullPath(), self.template_TPM_imported.fullPath())
  else:
    raise ValueError("Unvalid template_type")