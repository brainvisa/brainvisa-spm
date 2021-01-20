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
from shutil import copy2, copyfileobj
import gzip
from brainvisa.processes import *
from soma.spm.spm12.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.coregister import Estimate
from soma.spm.spm_launcher import SPM12, SPM12Standalone

configuration = Application().configuration


userLevel = 0
name = 'spm12 - Coregister: Estimate Only'

estimation_section = "Estimation options"
reslice_section = "reslice options"

signature = Signature(
    "reference", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
    "source", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
    "others", ListOf(ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    "objective_function", Choice("Mutual Information",
                                 "Normalised Mutual Information",
                                 "Entropy Correlation Coefficient",
                                 "Normalised Cross Correlation"),
    "separation", ListOf(Float()),
    "tolerances", ListOf(Float()),
    "histogram_smoothing", ListOf(Float()),

    "extract_coregister_matrix", Boolean(),
    "coregister_matrix", WriteDiskItem("Transformation matrix", "Transformation matrix"),
    
    # "output_type", Choice("In the same file"),
    "source_output", WriteDiskItem("4D Volume",
                                   ['NIFTI-1 image', 'SPM image', 'MINC image', 'gz compressed NIFTI-1 image']),
    "others_output", ListOf(WriteDiskItem("4D Volume",
                                          ['NIFTI-1 image', 'SPM image', 'MINC image', 'gz compressed NIFTI-1 image'])),

    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', section='default SPM outputs'),
)


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


def initialization(self):
    self.setOptional("others", "others_output")
    
    self.addLink(None, "extract_coregister_matrix", self.updateSignatureAboutCoregisterMatrix)
    
    self.linkParameters("source_output", "source")
    self.linkParameters("others_output", "others")

    self.addLink("batch_location", "source", self.updateBatchPath)

    self.objective_function = "Normalised Mutual Information"
    self.separation = [4, 2]
    self.tolerances = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]
    self.histogram_smoothing = [7, 7]
    self.extract_coregister_matrix = False


def updateSignatureAboutCoregisterMatrix(self, proc):
    if self.extract_coregister_matrix:
        self.setEnable("coregister_matrix")
    else:
        self.setDisable("coregister_matrix")
    self.signatureChangeNotifier.notify(self)


def updateBatchPath(self, proc):
    if self.source is not None:
        directory_path = os.path.dirname(self.source.fullPath())
        return os.path.join(directory_path, 'spm12_coregister_estimate_job.m')


def execution(self, context):
    try:
        source, others = self.generate_output(self.source, self.others,
                                              self.source_output, self.others_output)
        context.write(source)
        context.runProcess('SPM12CoregisterEstimate_generic',
                           reference=self.reference,
                           source=source,
                           others=others,
                           objective_function=self.objective_function,
                           separation=self.separation,
                           tolerances=self.tolerances,
                           histogram_smoothing=self.histogram_smoothing,
                           extract_coregister_matrix=self.extract_coregister_matrix,
                           coregister_matrix=self.coregister_matrix,
                           batch_location=self.batch_location)
        self.check_outputs(source, self.source_output, others, self.others_output)
    except ValueError:
        if source and os.path.exists(source):
            os.remove(source)
        if others:
            for oth in others:
                if os.path.exists(oth):
                    os.remove(oth)
    

def generate_output(self, source_diskitem, others_diskitem, source_output, others_output):
    """
    Create a copy of source/others images if output is different, to be used in SPM12Coregister.
    Handle .gz files.
    """
    source_current = self._gz_check_and_copy(source_diskitem, source_output)
    
    others_current = []
    for oth_disk, oth_out in zip(others_diskitem, others_output):
        oth_current = self._gz_check_and_copy(oth_disk, oth_out)
        others_current.append(oth_current)
    
    return source_current, others_current


def _gz_check_and_copy(self, disk, output):
    if os.path.splitext(output.fullPath())[-1] == '.gz':
        current = output.fullPath()[:-3]
    else:
        current = output.fullPath()
    
    if os.path.splitext(disk.fullPath())[-1] == '.gz':
        with gzip.open(disk.fullPath(), 'rb') as f_in:
            with open(current, 'wb') as f_out:
                copyfileobj(f_in, f_out)
    else:
        if disk.fullPath() != current:
            copy2(disk.fullPath(), current)
    return current


def check_outputs(self, source, source_output, others, others_output):
    self._check_output(source, source_output.fullPath())
    for oth, oth_output in zip(others, others_output):
        self._check_output(oth, oth_output.fullPath())


def _check_output(self, output_path, output_diskitem_path):
    """
    Checks if output has to be zipped.
    """
    if output_path != output_diskitem_path:
        if output_diskitem_path.endswith('.gz'):
            with open(output_path, 'rb') as f_in, gzip.open(output_diskitem_path, 'wb') as f_out:
                copyfileobj(f_in, f_out)
            os.remove(output_path)
        else:
            raise ValueError('Extension different between source and output. Only .gz supported.')
