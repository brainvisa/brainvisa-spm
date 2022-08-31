# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.tools.shoot_tools import WriteNormalised

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
name = 'SPM12 - Shoot - Write Normalised - generic'

signature = Signature(
    'final_space', Choice('MNI',
                          'Template'),
    'final_template', ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image']),
    'deformation_field', ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image']),
    'images', ListOf(ReadDiskItem(
        '4D Volume',
        ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    'images_warped', ListOf(WriteDiskItem(
        '4D Volume',
        ['NIFTI-1 image'])), #'gz compressed NIFTI-1 image'
    'voxel_sizes', ListOf(Float()),
    'bounding_box', Matrix(length=2, width=3),
    'preserve', Choice('Preserve Concentrations',
                       'Preserve Amount'),
    'fwhm', Float(),
    'batch_location', WriteDiskItem(
        'Matlab SPM script',
        'Matlab script',
        section='default SPM outputs'),
)


def initialization(self):
    self.setOptional('images_warped',
                     'bounding_box',
                     'voxel_sizes')
    self.addLink(None,
                 'final_space',
                 self.updateFinalTemplate)
    self.addLink('batch_location',
                 'deformation_field',
                 self.updateBatchPath)
    #SPM default initialisation
    #self.voxel_sizes = ['NaN', 'NaN', 'NaN']
    #self.bounding_box = [['NaN', 'NaN', 'NaN'],['NaN', 'NaN', 'NaN']]
    self.preserve = 'Preserve Concentrations'
    self.fwhm = 0


def updateFinalTemplate(self, final_space, names, parameterized):
    if final_space == 'MNI':
        self.setEnable('final_template')
    else:
        self.setDisable('final_template')
    self.changeSignature(self.signature)


def updateBatchPath(self, proc):
    if self.deformation_field is not None:
        dirname = os.path.dirname(self.deformation_field.fullPath())
        return os.path.join(dirname, 'spm12_shoot_write_normalised_job.m')


def execution(self, context):
    
    normalise = WriteNormalised()
    
    if self.final_space == 'MNI':
        normalise.setFinalTemplatePath(self.final_template.fullPath())
    normalise.setDeformationFieldPath(self.deformation_field.fullPath())
    normalise.setImagesPathList([image.fullPath() for image in self.images])
    if self.images_warped:
        normalise.setOutputImagesPathList([image_warped.fullPath() for image_warped in self.images_warped])

    if self.preserve == "Preserve Concentrations":
        normalise.setPreserveToConcentrations()
    elif self.preserve == "Preserve Amount":
        normalise.setPreserveToAmount()
    else:
        raise ValueError("Unvalid preserve")
    if self.voxel_sizes:
        normalise.setVoxelSizes(self.voxel_sizes)
    if self.bounding_box:
        normalise.setBoundingBox(numpy.array(self.bounding_box))
    normalise.setFWHM(self.fwhm)

    spm = validation()
    spm.addModuleToExecutionQueue(normalise)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
    
