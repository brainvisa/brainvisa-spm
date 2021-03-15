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
from brainvisa.processes import *
from soma.spm.spm12.spatial.normalise import EstimateAndWrite
from soma.spm.spm12.spatial.normalise.subject import SubjectToEstimateAndWrite
from soma.spm.spm12.spatial.normalise.writing_options import WritingOptions
from soma.spm.spm12.spatial.normalise.estimation_options import EstimationOptions
from soma.spm.spm_launcher import SPM12, SPM12Standalone

import os
import shutil
from tempfile import mkdtemp
import numpy


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
name = 'SPM12 - Normalise: Estimate & Write - generic'

subject_section = 'Subject options'
estimation_section = 'Estimation options'
writing_section = 'Writing options'
outputs_section = 'Outputs'

signature = Signature(
    'source', ReadDiskItem('4D Volume', 
                           ['NIFTI-1 image', 'gz compressed NIFTI-1 image',
                            'MINC image'], 
                           section=subject_section),
    'images_to_write', ListOf(ReadDiskItem('4D Volume', 
                                           ['NIFTI-1 image', 
                                            'gz compressed NIFTI-1 image',
                                            'MINC image']), 
                                           section=subject_section),


    'tpm_template', ReadDiskItem('TPM template', 
                                 ['NIFTI-1 image', 'SPM image', 'MINC image'], 
                                 section=estimation_section),
    'bias_regularisation', Choice('no regularisation (0)',
                                  'extremely light regularisation (0.00001)',
                                  'very light regularisation (0.0001)',
                                  'light regularisation (0.001)',
                                  'medium regularisation (0.01)',
                                  'heavy regularisation (0.1)',
                                  'very heavy regularisation (1)',
                                  'extremely heavy regularisation (10)', 
                                  section=estimation_section),
    'bias_fwhm', Choice('30mm cutoff', '40mm cutoff', '50mm cutoff',
                        '60mm cutoff', '70mm cutoff', '80mm cutoff',
                        '90mm cutoff', '100mm cutoff', '110mm cutoff',
                        '120mm cutoff', '130mm cutoff', '140mm cutoff',
                        '150mm cutoff', 'No correction', 
                        section=estimation_section),
    'warping_regularisation',ListOf(Float(), section=estimation_section),
    'affine_regularisation', Choice('No Affine Registration',
                                    'ICBM space template - European brains',
                                    'ICBM space template - East Asian brains',
                                    'Average sized template',
                                    'No regularisation', 
                                    section=estimation_section),
    'smoothness', Float(section=estimation_section),
    'sampling_distance', Float(section=estimation_section),
  
    'bounding_box', Matrix(length=2, width=3, section=writing_section),
    'voxel_size', ListOf(Float(),section=writing_section),
    'interpolation', Choice('Nearest neighbour',
                            'Trilinear',
                            '2nd Degree B-Spline',
                            '3rd Degree B-Spline',
                            '4th Degree B-Spline',
                            '5th Degree B-Spline',
                            '6th Degree B-Spline',
                            '7th Degree B-Spline',
                            section=writing_section),

    'custom_outputs', Boolean(section=outputs_section),
    'filename_prefix', String(section=outputs_section),
    'images_written', ListOf(WriteDiskItem('4D Volume', 
                                           ['gz compressed NIFTI-1 image', 
                                            'NIFTI-1 image']), 
                                           section=outputs_section),
    'forward_deformation_field', WriteDiskItem('4D Volume', 
                                               ['gz compressed NIFTI-1 image', 
                                                'NIFTI-1 image'], 
                                                section=outputs_section),
    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', 
                                    section=outputs_section),
)


def initialization(self):
    #SPM default initialisation
    self.tpm_template = self.signature['tpm_template'].findValue(
        {'template': 'TPM', 'SPM_version': '12'})
    self.bias_regularisation = 'very light regularisation (0.0001)'
    self.bias_fwhm = '60mm cutoff'
    self.warping_regularisation = [0, 0.001, 0.5, 0.05, 0.2]
    self.affine_regularisation = 'ICBM space template - European brains'
    self.smoothness = 0
    self.sampling_distance = 3
    self.bounding_box = [[-78, -112, -70],[78, 76, 85]]
    self.voxel_size = [2, 2, 2]
    self.interpolation = '4th Degree B-Spline'
    self.filename_prefix = 'w'
  
    self.setOptional('images_written')
    self.custom_outputs = False
    self.addLink(None, 'custom_outputs', 
                 self._updateSignatureAboutCustomOutputs)
    self.addLink(None, 'filename_prefix', self.checkIfNotEmpty)

    self.addLink('batch_location', 'source', self.updateBatchPath)


def _updateSignatureAboutCustomOutputs(self, proc):
    """Either use filename prefix for outputs or choose custom outputs."""
    if self.custom_outputs:
        self.setEnable('images_written')
        self.setDisable('filename_prefix')
    else:
        self.setDisable('images_written')
        self.setEnable('filename_prefix')
    self.signatureChangeNotifier.notify(self)
    

def checkIfNotEmpty(self, proc):
    if self.filename_prefix in [None, '']:
        self.filename_prefix = 'w'
    else:
        pass


def updateBatchPath(self, proc):
    if self.source is not None:
        directory_path = os.path.dirname(self.source.fullPath())
        return os.path.join(directory_path, 'spm12_normalise_EW_job.m')


def execution( self, context ):
    temp_directory = mkdtemp()
    try:
        # Gunzip input files if provided as .nii.gz
        source_ext = '.'.join(
            os.path.basename(self.source.fullPath()).split('.')[-2:])
        if source_ext == 'nii.gz':
            source_gz = shutil.copy(self.source.fullPath(), temp_directory)
            context.system('gunzip', source_gz)
            source = '.'.join(source_gz.split('.')[:-1])
        else:
            source = self.source.fullPath()
        
        images_to_write = []
        for image_to_write in self.images_to_write:
            if image_to_write.fullPath() != self.source.fullPath():
                image_ext = '.'.join(os.path.basename(
                    image_to_write.fullPath()).split('.')[-2:])
                if image_ext == 'nii.gz':
                    image_gz = shutil.copy(image_to_write.fullPath(), 
                                           temp_directory)
                    context.system('gunzip', image_gz)
                    image = '.'.join(image_gz.split('.')[:-1])
                else:
                    image = image_to_write.fullPath()
            else:
                image = source
            images_to_write.append(image)
        
        estimate_and_write = EstimateAndWrite()
    
        # Set subject information
        subject = SubjectToEstimateAndWrite()
        subject.setImagesToAlign(source)
        subject.setImageListToWrite(images_to_write)
#        subject.setImagesToAlign(self.source.fullPath())
#        subject.setImageListToWrite(
#            [diskitem.fullPath() for diskitem in self.images_to_write])
        if self.images_written:
            subject.setImageListWritten(
            [diskitem.fullPath() for diskitem in self.images_written])
        if self.forward_deformation_field is not None:
            subject.setForwardDeformationField(
                self.forward_deformation_field.fullPath())
    
        estimate_and_write.appendSubject(subject)
    
        # Set estimation options
        estimate = EstimationOptions()
        estimate.setTpm(self.tpm_template.fullPath())
        estimate.setBiasRegularisation(
            float(self.bias_regularisation.split('(')[1].strip(')')))
        if self.bias_fwhm == 'No correction':
            estimate.unsetBiasFwhm()
        else:
            estimate.setBiasFwhm(int(self.bias_fwhm.split()[0].strip('m')))
        if self.affine_regularisation == \
          'ICBM space template - European brains':
            estimate.setAffineRegularisationToEuropeanBrains()
        elif self.affine_regularisation == \
          'ICBM space template - East Asian brains':
            estimate.setAffineRegularisationToAsianBrains()
        elif self.affine_regularisation == 'Average sized template':
            estimate.setAffineRegularisationToAverageSizedTemplate()
        elif self.affine_regularisation == 'No Affine Registration':
            estimate.unsetAffineRegularisation() 
        elif self.affine_regularisation == 'No regularisation':
            estimate.unsetRegularisation()
        estimate.setWarpingRegularisation(self.warping_regularisation)
        estimate.setSmoothness(self.smoothness)
        estimate.setSamplingDistance(self.sampling_distance)
    
        estimate_and_write.estimation_options = estimate
    
        # Set writing options
        writing = WritingOptions()
    
        writing.setBoundingBox(numpy.array(self.bounding_box))
        writing.setVoxelSize(self.voxel_size)
    
        if self.interpolation == 'Nearest neighbour':
            writing.setInterpolation(0)
        elif self.interpolation == 'Trilinear':
            writing.setInterpolation(1)
        else:
            writing.setInterpolation(
                int(self.interpolation.split()[0].strip('ndth')))
    
        writing.setFilenamePrefix(self.filename_prefix)
    
        estimate_and_write.writing_options = writing
    
        # Run script
        spm = validation()
        spm.addModuleToExecutionQueue(estimate_and_write)
        spm.setSPMScriptPath(self.batch_location.fullPath())
        output = spm.run()
        context.log(name, html=output)
    finally:
#        print(temp_directory)
        shutil.rmtree(temp_directory)
