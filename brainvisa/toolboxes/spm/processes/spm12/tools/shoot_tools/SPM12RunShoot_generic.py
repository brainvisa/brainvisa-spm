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
from brainvisa.tools import spm_utils
from brainvisa.processes import *
import os
import shutil
from distutils.dir_util import copy_tree
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.tools.shoot_tools import RunShoot

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
name = 'SPM12 - Run Shoot - generic'

SIGNATURE_BEGIN = ["nb_images", Integer()]
SIGNATURE_END = [
    "templates", ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    
    "custom_outputs", Boolean(),
    
    "jacobian_outputs", ListOf(WriteDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    "velocity_outputs", ListOf(WriteDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    "deformation_outputs", ListOf(WriteDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    
    "batch_location", WriteDiskItem('Matlab SPM script', 'Matlab script'),
]

signature_params = SIGNATURE_BEGIN + ["images_1", ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']))] + SIGNATURE_END
signature = Signature(*signature_params)


def initialization(self):
    self.nb_images = 1
    self.addLink('batch_location', 'images_1', self.update_batch_path)
    self.addLink(None, 'nb_images', self.update_nb_images)
    self.addLink(None, 'custom_outputs', self.update_outputs_choice)
    self.custom_outputs = False


def update_batch_path(self, proc):
    """
    Place batch file next to the first image of image_1 param
    """
    if self.images_1:
        directory_path = os.path.dirname(self.images_1[0].fullPath())
        return os.path.join(directory_path, 'spm12_shoot_job.m')


def update_nb_images(self, proc):
    new_signature = list(SIGNATURE_BEGIN)
    for i in range(proc):
        new_signature += ["images_%d" % (i + 1),
                          ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']))]
    new_signature += SIGNATURE_END
    signature = Signature(*new_signature)
    self.changeSignature(signature)


def update_outputs_choice(self, proc):
    if proc:
        self.setEnable('jacobian_outputs', 'velocity_outputs', 'deformation_outputs')
    else:
        self.setDisable('jacobian_outputs', 'velocity_outputs', 'deformation_outputs')
    self.changeSignature(self.signature)


def execution(self, context):
    
    run_shoot = RunShoot()
    t = []
    for i in range(1, self.nb_images + 1):
        t.append([im.fullPath() for im in getattr(self, 'images_%d' % i)])
    run_shoot.images_path_list = t
    run_shoot.templates_path_list = [template.fullPath() for template in self.templates]
    
    if self.custom_outputs:
        run_shoot.jacobian_output_path_list = [j.fullPath() for j in self.jacobian_outputs]
        run_shoot.velocity_output_path_list = [v.fullPath() for v in self.velocity_outputs]
        run_shoot.deformation_output_path_list = [d.fullPath() for d in self.deformation_outputs]
    
    spm = validation()
    spm.addModuleToExecutionQueue(run_shoot)
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)
