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
# and INRIA at the following URL 'http://www.cecill.info'.
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

from brainvisa.processes import *

from soma.spm.spm12.spatial.realign.reslice_options import ResliceOptions
from soma.spm.spm12.spatial.realign.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.realign import EstimateAndReslice
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
name = 'spm12 - Realign: Estimate & Reslice - generic'

input_section = 'Inputs'
data_section = 'Data'
estimation_section = 'Estimation options'
reslice_section = 'Reslice options'
output_section = 'Outputs'


signature = Signature(
    'session_paths_0', ListOf(ReadDiskItem('4D Volume', 
                                           ['NIFTI-1 image', 'SPM image', 
                                            'MINC image']), 
                                           section=input_section),
    'session_paths_1', ListOf(ReadDiskItem('4D Volume', 
                                           ['NIFTI-1 image', 'SPM image', 
                                            'MINC image']), 
                                           section=input_section),

    'quality', Float(section=estimation_section),
    'separation', Float(section=estimation_section),
    'smoothing', Float(section=estimation_section),
    'num_passes', Choice('Register to first', 'Register to mean', 
                         section=estimation_section),
    'interpolation', Choice('Nearest neighbour',
                            'Trilinear',
                            '2nd Degree B-Spline',
                            '3rd Degree B-Spline',
                            '4th Degree B-Spline',
                            '5th Degree B-Spline',
                            '6th Degree B-Spline',
                            '7th Degree B-Spline',
                            section=estimation_section),
    'wrapping', Choice(('No wrap', [False, False, False]),
                       ('Wrap X', [True, False, False]),
                       ('Wrap Y', [False, True, False]),
                       ('Wrap X & Y', [True, True, False]),
                       ('Wrap Z', [False, False, True]),
                       ('Wrap X & Z', [True, False, True]),
                       ('Wrap Y & Z', [False, True, True]),
                       ('Wrap X, Y & Z', [True, True, True]),
                       section=estimation_section),
    'weighting', ReadDiskItem('4D Volume', 
                              ['NIFTI-1 image', 'SPM image', 'MINC image'], 
                              section=estimation_section),

    'resliced_images', Choice('All Images (1..n)',
                              'Images 2..n',
                              'All Images + Mean Image',
                              'Mean Image Only',
                              section=reslice_section),

    'resliced_interpolation', Choice('Nearest neighbour',
                                     'Trilinear',
                                     '2nd Degree B-Spline',
                                     '3rd Degree B-Spline',
                                     '4th Degree B-Spline',
                                     '5th Degree B-Spline',
                                     '6th Degree B-Spline',
                                     '7th Degree B-Spline',
                                     section=reslice_section),
    'resliced_wrapping', Choice(('No wrap', [False, False, False]),
                                ('Wrap X', [True, False, False]),
                                ('Wrap Y', [False, True, False]),
                                ('Wrap X & Y', [True, True, False]),
                                ('Wrap Z', [False, False, True]),
                                ('Wrap X & Z', [True, False, True]),
                                ('Wrap Y & Z', [False, True, True]),
                                ('Wrap X, Y & Z', [True, True, True]),
                                section=reslice_section),
    'masking', Boolean(section=reslice_section),
    'filename_prefix', String(section=reslice_section),

    'realign_paths_0', ListOf(WriteDiskItem('4D Volume', 
                                            ['gz compressed NIFTI-1 image', 
                                             'NIFTI-1 image']), 
                                            section=output_section),
    'realign_paths_1', ListOf(WriteDiskItem('4D Volume', 
                                            ['gz compressed NIFTI-1 image', 
                                             'NIFTI-1 image']), 
                                            section=output_section),
    'ouput_mean', WriteDiskItem('4D Volume', 
                                ['gz compressed NIFTI-1 image', 
                                 'NIFTI-1 image'], 
                                section=output_section),
    'realign_parameters', ListOf(WriteDiskItem('Text file', 'Text file'), 
                                 section=output_section),

    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', 
                                    section='default SPM outputs' ),
)


def initialization(self):
    self.setOptional('weighting', 'ouput_mean', 'realign_parameters',
                     'session_paths_1', 'realign_paths_0', 'realign_paths_1')

    self.addLink(None, 'filename_prefix', self.checkIfNotEmpty)

    self.addLink('batch_location', 'session_paths_0', self.updateBatchPath)

    #SPM default initialisation
    self.quality = 0.9
    self.separation = 4
    self.smoothing = 5
    self.num_passes = 'Register to mean'
    self.interpolation = '2nd Degree B-Spline'
    self.wrapping = 'No wrap'

    self.resliced_images = 'All Images + Mean Image'
    self.resliced_interpolation = '4th Degree B-Spline'
    self.resliced_wrapping = 'No wrap'
    self.masking = True
    self.filename_prefix = 'r'


def checkIfNotEmpty(self, proc):
    if self.filename_prefix in [None, '']:
        self.filename_prefix = 'r'


def updateBatchPath(self, proc):
    if self.session_paths_0:
        directory_path = os.path.dirname(self.session_paths_0[0].fullPath())
        return os.path.join(directory_path, 'spm12_realign_ER_job.m')


def execution( self, context ):
    # Set estimation options
    estimation_options = EstimationOptions()
    estimation_options.setQuality(self.quality)
    estimation_options.setSeparation(self.separation)
    estimation_options.setSmoothingFWHM(self.smoothing)

    if self.num_passes == 'Register to first':
        estimation_options.setNumPassesToRegisterToFirst()
    elif self.num_passes == 'Register to mean':
        estimation_options.setNumPassesToRegisterToMean()
    else:
        raise ValueError('Unvalid num_passes')

    if self.interpolation == 'Nearest neighbour':
        estimation_options.setInterpolationToNearestNeighbour()
    elif self.interpolation == 'Trilinear':
        estimation_options.setInterpolationToTrilinear()
    elif self.interpolation == '2nd Degree B-Spline':
        estimation_options.setInterpolationTo2ndDegreeBSpline()
    elif self.interpolation == '3rd Degree B-Spline':
        estimation_options.setInterpolationTo3rdDegreeBSpline()
    elif self.interpolation == '4th Degree B-Spline':
        estimation_options.setInterpolationTo4thDegreeBSpline()
    elif self.interpolation == '5th Degree B-Spline':
        estimation_options.setInterpolationTo5thDegreeBSpline()
    elif self.interpolation == '6th Degree B-Spline':
        estimation_options.setInterpolationTo6thDegreeBSpline()
    elif self.interpolation == '7th Degree B-Spline':
        estimation_options.setInterpolationTo7thDegreeBSpline()
    else:
        raise ValueError('Unvalid interpolation')

    estimation_options.setWrapping(self.wrapping[0], 
                                   self.wrapping[1], 
                                   self.wrapping[2])
    if self.weighting is not None:
        estimation_options.setWeighting(self.weighting.fullPath())

    # Set reslice options
    reslice_options = ResliceOptions()
    if self.resliced_images == 'All Images (1..n)':
        reslice_options.setReslicedImagesToAllImages
    elif self.resliced_images == 'Images 2..n':
        reslice_options.setReslicedImagesToImagesExceptFirst()
    elif self.resliced_images == 'All Images + Mean Image':
        reslice_options.setReslicedImagesToAllImagesAndMeanImage()
    elif self.resliced_images == 'Mean Image Only':
        reslice_options.setReslicedImagesToMeanImageOnly()
    else:
        raise ValueError('Unvalid resliced_images')

    if self.resliced_interpolation == 'Nearest neighbour':
        reslice_options.setInterpolationToNearestNeighbour()
    elif self.resliced_interpolation == 'Trilinear':
        reslice_options.setInterpolationToTrilinear()
    elif self.resliced_interpolation == '2nd Degree B-Spline':
        reslice_options.setInterpolationTo2ndDegreeBSpline()
    elif self.resliced_interpolation == '3rd Degree B-Spline':
        reslice_options.setInterpolationTo3rdDegreeBSpline()
    elif self.resliced_interpolation == '4th Degree B-Spline':
        reslice_options.setInterpolationTo4thDegreeBSpline()
    elif self.resliced_interpolation == '5th Degree B-Spline':
        reslice_options.setInterpolationTo5thDegreeBSpline()
    elif self.resliced_interpolation == '6th Degree B-Spline':
        reslice_options.setInterpolationTo6thDegreeBSpline()
    elif self.resliced_interpolation == '7th Degree B-Spline':
        reslice_options.setInterpolationTo7thDegreeBSpline()
    else:
        raise ValueError('Unvalid resliced_interpolation')

    reslice_options.setWrapping(self.resliced_wrapping[0],
                                self.resliced_wrapping[1],
                                self.resliced_wrapping[2])

    if self.masking:
        reslice_options.setMasking()
    else:
        reslice_options.unsetMasking()

    reslice_options.setFilenamePrefix(self.filename_prefix)  

    # Set input/outputs
    estimate_and_reslice = EstimateAndReslice()
    estimate_and_reslice.addSessionPathList(
        [diskitem.fullPath() for diskitem in self.session_paths_0])
    if self.session_paths_1:
        estimate_and_reslice.addSessionPathList(
            [diskitem.fullPath() for diskitem in self.session_paths_1])

    if self.realign_paths_0 is not None:
        estimate_and_reslice.addSessionRealignedPathList(
            [diskitem.fullPath() for diskitem in self.realign_paths_0])

    if None not in [self.session_paths_1, self.realign_paths_1]:
        estimate_and_reslice.addSessionRealignedPathList(
            [diskitem.fullPath() for diskitem in self.realign_paths_1])

    if self.ouput_mean is not None:
        estimate_and_reslice.setMeanOuputPath(self.ouput_mean.fullPath())

    if self.realign_parameters:
        for diskitem in self.realign_parameters:
            estimate_and_reslice.addSessionRealignmentParametersPath(
                diskitem.fullPath())

    # Run process
    estimate_and_reslice.replaceEstimationOptions(estimation_options)
    estimate_and_reslice.replaceResliceOptions(reslice_options)

    spm = validation()
    spm.addModuleToExecutionQueue(estimate_and_reslice)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)

