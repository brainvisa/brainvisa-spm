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
import tempfile
import numpy as np
from soma.spm.spm12.util.deformations import Composition, Deformations
from soma.spm.spm12.util.deformations.composition import MatFileImported
# from soma.spm.spm12.util.deformations.composition import DartelFlow
from soma.spm.spm12.util.deformations.composition import DeformationField
# from soma.spm.spm12.util.deformations.composition import IdentityFromImage
# from soma.spm.spm12.util.deformations.composition import Identity
from soma.spm.spm12.util.deformations.composition import Inverse
from soma.spm.spm12.util.deformations.output import PullBack, PushForward
from soma.spm.spm_batch_maker_utils import copyNifti
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

inputs = 'Inputs'
options = 'Options'
pull_options = 'Pullback options'
push_options = 'Pushforward options'
outputs = 'Outputs'
userLevel = 1
name = 'spm12 - Deformations : apply one deformation - generic'

signature = Signature(
    'input_images', ListOf(ReadDiskItem(
        '4D Volume', #TODO : modify because 4D is unvailable from SPM
        ['NIFTI-1 image', 'SPM image', 'MINC image']),
        section=inputs),
    'deformation_type', Choice(
        ('Deformation field', 'deformation_field'),
        ('Spatial normalisation (_sn.mat)', 'spatial_normalisation_param'),
        section=inputs),
    'deformation_field', ReadDiskItem(
        '4D Volume',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image', 'SPM image', 'MINC image'],
        section=inputs),
    'spatial_normalisation_param', ReadDiskItem(
        'SPM transformation',
        ['Matlab file'],
        section=inputs),
    'voxel_sizes', ListOf(Float(), section=inputs),
    'bounding_box', Matrix(length=2, width=3, section=inputs),
    'apply_inverse', Boolean(section=inputs),
    'inverse_reference_volume', ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image'],
        section=inputs),
    'outputs_method', Choice('Pullback',
                             'Pushforward',
                             section=inputs),
    #pull options
    'interpolation', Choice('Nearest neighbour',
                            'Trilinear',
                            '2nd Degree B-Spline',
                            '3rd Degree B-Spline',
                            '4th Degree B-Spline',
                            '5th Degree B-Spline',
                            '6th Degree B-Spline',
                            '7th Degree B-Spline',
                            section=pull_options),
    'masking', Boolean(section=pull_options),
    #push options
    'weight_image', ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image'],
        section=push_options),
    'fov_ref_image', ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image'],
        section=push_options),
    'fov_voxel_sizes', ListOf(Float(), section=push_options),
    'fov_bounding_box', Matrix(length=2, width=3, section=push_options),
    'preserve', Choice(('Preserve Concentrations (no modulation)', 'no_mod'),
                       ('Preserve Amount (modulation)', 'mod'),
                       ('Preserve labels (categorical data)', 'labels'),
                       section=push_options),
    'gaussian_fwhm', ListOf(Float(), section=options),
    'output_destination', Choice('Current directory',
                                 'Source directories',
                                 'Output directory',
                                 section=outputs),
    'ouput_directory', WriteDiskItem(
        'Directory',
        'Directory',
        section=outputs),
    'custom_outputs', Boolean(section=outputs),
    'images_deformed', ListOf(WriteDiskItem(
        '4D Volume',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
        section=outputs),
    #Batch
    'batch_location', WriteDiskItem(
        'Matlab SPM script',
        'Matlab script',
        section=outputs)
)

def initialization(self):
    self.addLink(None, 'deformation_type', self.updateSignatureAboutDeformation)
    self.addLink(None, 'apply_inverse', self.updateSignatureAboutInverse)
    self.addLink(None, 'outputs_method', self.updateSignatureAboutMethod)
    self.addLink(None, 'custom_outputs', self.updateSignatureAboutOutputs)
    self.addLink(None, 'output_destination', self.updateSignatureAboutOutputDestination)

    self.addLink("batch_location", "deformation_field", self.updateBatchPath)

    # self.voxel_sizes = [np.nan, np.nan, np.nan]
    # self.bounding_box = [[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]]
    self.apply_inverse = False
    self.outputs_method = 'Pullback'
    self.interpolation = '4th Degree B-Spline'
    self.preserve = 'no_mod'
    self.gaussian_fwhm = [0, 0, 0]
    self.custom_outputs = False


def updateSignatureAboutDeformation(self, proc):
    for _, param in self.signature['deformation_type'].values:
        if param == self.deformation_type:
            self.setEnable(param)
        else:
            self.setDisable(param)
    if self.deformation_type == 'spatial_normalisation_param':
        self.setEnable('voxel_sizes', 'bounding_box')
        self.setOptional('voxel_sizes', 'bounding_box')
    else:
        self.setDisable('voxel_sizes', 'bounding_box')
    self.changeSignature(self.signature)

def updateSignatureAboutInverse(self, proc):
    if self.apply_inverse:
        self.setEnable('inverse_reference_volume')
    else:
        self.setDisable('inverse_reference_volume')
    self.changeSignature(self.signature)

def updateSignatureAboutMethod(self, proc):
    if self.outputs_method == 'Pullback':
        self.setEnable('interpolation', 'masking')
        self.setDisable('weight_image', 'fov_ref_image',
                        'fov_voxel_sizes', 'fov_bounding_box',
                        'preserve')
    else:
        self.setEnable('weight_image', 'fov_ref_image',
                       'fov_voxel_sizes', 'fov_bounding_box',
                       'preserve')
        self.setOptional('weight_image', 'fov_ref_image',
                         'fov_voxel_sizes', 'fov_bounding_box')
        self.setDisable('interpolation', 'masking')
    self.changeSignature(self.signature)

def updateSignatureAboutOutputs(self, proc):
    if self.custom_outputs:
        self.setEnable('images_deformed')
    else:
        self.setDisable('images_deformed')
    self.changeSignature(self.signature)

def updateSignatureAboutOutputDestination(self, proc):
    if self.output_destination == 'Output directory':
        self.setEnable('ouput_directory')
    else:
        self.setDisable('ouput_directory')
    self.changeSignature(self.signature)

def updateBatchPath(self, proc):
    if self.deformation_field is not None:
        ouput_directory = os.path.dirname(self.deformation_field.fullPath())
        return os.path.join(ouput_directory, 'spm12_deformations_job.m')

def execution(self, context):
    
    if self.deformation_type == 'spatial_normalisation_param':
        matfile_imported = MatFileImported()
        matfile_imported.setParameterFile(self.spatial_normalisation_param.fullPath())
        if self.voxel_sizes:
            matfile_imported.setVoxelSize(self.voxel_sizes)
        if self.bounding_box:
            matfile_imported.setBoundingBox(np.array(self.bounding_box))
        deformation_element = matfile_imported
    else:
        if str(self.deformation_field.format) == "gz compressed NIFTI-1 image":
            deformation = context.temporary('NIFTI-1 image', prefix='y_bv')
            deformation_fullpath = deformation.fullPath()
            copyNifti(self.deformation_field.fullPath(), deformation_fullpath)
        else:
            deformation_fullpath = self.deformation_field.fullPath()

        deformation_field = DeformationField()
        deformation_field.setDeformationFieldPath(deformation_fullpath)
        deformation_element = deformation_field

    deformations = Deformations()
    if self.apply_inverse:
        comp = Composition()
        comp.append(deformation_element)
        inverse = Inverse()
        inverse.setDeformationComposition(comp)
        inverse.setImageToBaseInverseOn(self.reference_volume.fullPath())
        deformations.appendDeformation(inverse)
    else:
        deformations.appendDeformation(deformation_element)

    if self.outputs_method == 'Pullback':
        pback = PullBack()
    else:
        pback = PushForward()
    
    pback.setVolumeListToApply([diskitem.fullPath() for diskitem in self.input_images])

    if self.custom_outputs:
        pback.setOuputPathList([diskitem.fullPath() for diskitem in self.images_deformed])

    if self.output_destination == 'Current directory':
        # deformations.setOuputDestinationToCurrentDirectory()#SPM current directory == batch directory
        pback.setOutputDestinationToOutputDirectory(os.path.dirname(self.batch_location.fullPath()))
    elif self.output_destination == 'Source directories':
        pback.setOuputDestinationToSourceDirectories()
    elif self.output_destination == 'Output directory':
        if not os.path.exists(self.ouput_directory.fullPath()):
            os.makedirs(self.ouput_directory.fullPath())
        else:
            pass#directory already exists
        pback.setOutputDestinationToOutputDirectory(self.ouput_directory.fullPath())
    else:
        raise ValueError("Unvalid output_destination")
    
    if self.outputs_method == 'Pullback':
        if self.interpolation == "Nearest neighbour":
            pback.setInterpolationToNearestNeighbour()
        elif self.interpolation == "Trilinear":
            pback.setInterpolationToTrilinear()
        elif self.interpolation == "2nd Degree B-Spline":
            pback.setInterpolationTo2ndDegreeBSpline()
        elif self.interpolation == "3rd Degree B-Spline":
            pback.setInterpolationTo3rdDegreeBSpline()
        elif self.interpolation == "4th Degree B-Spline":
            pback.setInterpolationTo4thDegreeBSpline()
        elif self.interpolation == "5th Degree B-Spline":
            pback.setInterpolationTo5thDegreeBSpline()
        elif self.interpolation == "6th Degree B-Spline":
            pback.setInterpolationTo6thDegreeBSpline()
        elif self.interpolation == "7th Degree B-Spline":
            pback.setInterpolationTo7thDegreeBSpline()
        else:
            raise ValueError("Unvalid interpolation")

        if self.masking:
            pback.setMasking()
        else:
            pback.unsetMasking()
    else:
        if self.weight_image:
            pback.setWeightImagePath(self.weight_image.fullPath())
        
        if self.fov_ref_image:
            pback.setFieldOfViewToImageDefined(self.fov_ref_image.fullPath())
        elif self.fov_voxel_sizes and self.fov_bounding_box:
            pback.setFieldOfViewToUserDefined(np.array(self.fov_bounding_box),
                                              self.fov_voxel_sizes)
        else:
            raise ValueError("Unvalid FOV, an image reference or the bounding_box and voxel_sizes of the output must be fill")
        
        if self.preserve == 'no_mod':
            pback.setPreserveToConcentrations()
        elif self.preserve == 'mod':
            pback.setPreserveToAmount()
        else:
            raise ValueError("Unvalid preserve option")

    if len(self.gaussian_fwhm) == 3:
        pback.setFWHM(self.gaussian_fwhm[0],
                      self.gaussian_fwhm[1],
                      self.gaussian_fwhm[2])
    else:
        context.error("gaussian_fwhm requires 3 value")

    deformations.appendOutput(pback)

    spm = validation()
    spm.addModuleToExecutionQueue(deformations)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
