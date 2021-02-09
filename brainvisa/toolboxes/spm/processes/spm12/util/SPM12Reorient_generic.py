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
import os
from brainvisa.processes import Application, Signature, ListOf, ReadDiskItem, WriteDiskItem
from brainvisa.processes import Choice, Float, String, Matrix, Boolean
from soma.spm.spm12.util.reorient import Reorient
from soma.spm.spm_launcher import SPM12, SPM12Standalone

configuration = Application().configuration


def validation():
    try:
        spm = SPM12Standalone(configuration.SPM.spm12_standalone_command,
                              configuration.SPM.spm12_standalone_mcr_path,
                              configuration.SPM.spm12_standalone_path)
    except Exception:
        spm = SPM12(configuration.SPM.spm12_path,
                    configuration.matlab.executable,
                    configuration.matlab.options)
    return spm


userLevel = 1
name = 'spm12 - Reorient - generic'

signature = Signature(
    "images_to_reorient", ListOf(ReadDiskItem('4D Volume',
                                              ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    "reorient_by", Choice(("Reorientation Matrix", 'matrix'),
                          ("Reorientation Parameters", 'parameters'),
                          ("Saved reorientation matrix", 'saved_matrix')),
    "matrix", Matrix(length=4, width=4),
    "parameters", ListOf(Float()),
    "saved_matrix", ReadDiskItem('Matlab SPM script', 'Matlab file'),
    "custom_outputs", Boolean(),
    "filename_prefix", String(),
    "images_reoriented", ListOf(WriteDiskItem('4D Volume',
                                              ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
    "batch_location", WriteDiskItem('Matlab SPM script', 'Matlab script'),
)


def initialization(self):
    self.setDisable('parameters', 'saved_matrix')
    self.addLink(None, "reorient_by", self.update_reorient_method)
    self.addLink('batch_location', 'images_to_reorient', self.update_batch_path)
    
    self.setOptional('filename_prefix', 'images_reoriented')
    self.custom_outputs = False
    self.addLink(None, 'custom_outputs', 
                 self._updateSignatureAboutCustomOutputs)


def update_reorient_method(self, proc):
    self.setDisable('matrix', 'parameters', 'saved_matrix')
    self.setEnable(self.reorient_by)
    self.changeSignature(self.signature)


def update_batch_path(self, proc):
    """
    Place batch file next to the first image of images_to_reorient param
    """
    if self.images_to_reorient:
        image_dirname = os.path.dirname(self.images_to_reorient[0].fullPath())
        return os.path.join(image_dirname, 'spm12_reorient_job.m')
    else:
        return None


def _updateSignatureAboutCustomOutputs(self, proc):
    """Either use filename prefix for outputs or choose custom outputs."""
    if self.custom_outputs:
        self.setEnable('images_reoriented')
        self.setDisable('filename_prefix')
    else:
        self.setDisable('images_reoriented')
        self.setEnable('filename_prefix')
    self.signatureChangeNotifier.notify(self)
    

def execution(self, context):
    reorient = Reorient()
    
    reorient.set_images_path_list([image.fullPath() for image in self.images_to_reorient])
    
    if self.reorient_by == 'matrix':
        reorient.set_reorient_by_reorient_matrix()
        reorient.set_reorient_matrix(list(self.matrix))
    elif self.reorient_by == 'parameters':
        reorient.set_reorient_by_reorient_parameters()
        reorient.set_reorient_parameters(self.parameters)
    elif self.reorient_by == 'saved_matrix':
        reorient.set_reorient_by_saved_matrix()
        reorient.set_saved_matrix(self.saved_matrix.fullPath())
    
    if self.custom_outputs:
        reorient.set_prefix('o')
        reorient.set_output_images_path_list(
            [image.fullPath() for image in self.images_reoriented])
    else:
        if self.filename_prefix is not None:
            reorient.set_prefix(self.filename_prefix)
    
    spm = validation()
    spm.addModuleToExecutionQueue(reorient)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
