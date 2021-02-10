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
import numpy as np

from brainvisa.processes import *

from soma import aims
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.tools.slice_timing import SliceTiming
import soma.spm.spm12.tools.slice_timing.utils as st_utils

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
name = 'SPM12 - Slice Timing - generic'

signature = Signature(
    'input_image', ReadDiskItem('4D Volume', 
                                 ['NIFTI-1 image', 'SPM image', 'MINC image']),
    'acquisition_direction', Choice('Axial', 'Coronal', 'Sagittal'),
    'manufacturer', Choice('', 'Siemens', 'Philips'),
    'slice_order_type', Choice(''),
    'reference_slice_type', Choice('', 'First', 'Middle', 'Last'),
    'custom_outputs', Boolean(),
    'filename_prefix', String(),
    'output_image', WriteDiskItem('4D Volume', 
                                  ['gz compressed NIFTI-1 image', 
                                   'NIFTI-1 image']),
    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script')
)


def initialization(self):
    self.acquisition_direction = 'Axial'
    
    self.manufacturer = ''    
    self.addLink(None, 'manufacturer', self._updateSliceOrderChoices)
    
    self.setOptional('output_image')

    self.custom_outputs = False
    self.addLink(None, 'custom_outputs', 
                 self._updateSignatureAboutCustomOutputs)

    self.filename_prefix = 'a'
    self.addLink(None, 'filename_prefix', self._checkIfNotEmpty)

    self.addLink('batch_location', 'input_image', self._updateBatchPath)


def _updateSliceOrderChoices(self, proc):
    """Set slice order choice list from scanner's manufacturer."""
    choices = ['']
    if self.manufacturer == 'Siemens':
        choices = ['', 'Ascending sequential', 'Descending sequential', 
                   'Ascending interleaved']
    elif self.manufacturer == 'Philips':
        choices = ['', 'Interleaved Single package?']
    self.signature['slice_order_type'].setChoices(*choices)
    
    
def _updateSignatureAboutCustomOutputs(self, proc):
    """Either use filename prefix for outputs or choose custom outputs."""
    if self.custom_outputs:
        self.setEnable('output_image')
        self.setDisable('filename_prefix')
    else:
        self.setDisable('output_image')
        self.setEnable('filename_prefix')
    self.signatureChangeNotifier.notify(self)


def _checkIfNotEmpty(self, proc):
    """Force a value for the filename prefix if empty."""
    if self.filename_prefix in [None, '']:
        self.filename_prefix = 'a'


def _updateBatchPath(self, proc):
    """Place batch file next to the first input image."""
    if (self.input_image is not None) and \
       (os.path.exists(self.input_image.fullPath())):
        
        directory_path = os.path.dirname(self.input_image.fullPath())
        return os.path.join(directory_path, 'spm12_slice_timing_job.m')


def execution(self, context):
    slice_timing = SliceTiming()

    # Compute relevant parameters from input
    input_array = np.array(aims.read(self.input_image.fullPath()), copy=False)
    acq = ['Sagittal', 'Coronal', 'Axial'].index(self.acquisition_direction)
    number_of_slices = input_array.shape[acq]
    
    tr = st_utils.get_tr(self.input_image.fullPath())
    
    ta = tr - (float(tr) / number_of_slices)
    
    slice_order = st_utils.get_slice_order(number_of_slices,
                                           self.slice_order_type,
                                           self.manufacturer)
    
    reference_slice_index = st_utils.st_get_ref_slice(
        self.reference_slice_type, slice_order)
    
    # Set parameters in SPM process
    slice_timing.setInputImagesPathList(
        st_utils.getSpmImagesListFrom4DVolume(self.input_image.fullPath()))        
    slice_timing.setNumberOfSlices(number_of_slices)
    slice_timing.setRepetitionTime(tr)
    slice_timing.setAcquisitionTime(ta)
    slice_timing.setSliceOrder(slice_order)
    slice_timing.setReferenceSliceIndex(reference_slice_index)
    slice_timing.setFilenamePrefix(self.filename_prefix)
    
    if self.custom_outputs:
        slice_timing.setOuputImagePath(self.output_image.fullPath())

    # Run process
    spm = validation()
    spm.addModuleToExecutionQueue(slice_timing)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
    
    # Update output header
    if self.custom_outputs:
        output_path = self.output_image.fullPath()
    else:
        output_directory = os.path.dirname(self.input_image.fullPath())
        output_name = self.filename_prefix + \
                      os.path.basename(self.input_image.fullPath())
        output_path = os.path.join(output_directory, output_name)
    output_volume = aims.read(output_path)
    output_volume.header().update(
        aims.read(self.input_image.fullPath()).header())
    aims.write(output_volume, output_path)
