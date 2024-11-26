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


userLevel = 0
name = 'spm12 - serial longitudinal registration'


signature = Signature(
    'modality', Choice(('T1 MRI', ['Raw T1 MRI', 'T1 MRI mid-point average']),
                       ('FLAIR MRI', ['Raw FLAIR MRI', 'FLAIR MRI mid-point average'])),
    'volumes', ListOf(ReadDiskItem('Raw T1 MRI', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    'times', ListOf(Float()),
    'noise_estimate', Choice("NaN", "Scalar", "Matrix"),
    'noise_estimate_value', Matrix(),
    'warping_regularisation', ListOf(Float()),
    'bias_regularisation', Float(),
    'customs_outputs', Boolean(),
    'save_MPA', Boolean(),
    'MPA', WriteDiskItem('T1 MRI mid-point average', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                         requiredAttributes={'processing': 'spm12Serial'}),
    'save_jacobians', Boolean(),
    'jacobians', ListOf(WriteDiskItem('Jacobian determinant', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                          requiredAttributes={'processing': 'spm12Serial'})),
    'save_divergences', Boolean(),
    'divergences', ListOf(WriteDiskItem('Divergence map', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                            requiredAttributes={'processing': 'spm12Serial'})),
    'save_deformation_fields', Boolean(),
    'deformation_fields', ListOf(WriteDiskItem('SPM deformation field',
                                               ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                               requiredAttributes={'processing': 'spm12Serial',
                                                                   'orientation': 'acquisition_to_average',
                                                                   'direction': 'forward',
                                                                   'warping_method': 'none'})),
    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', section='default SPM outputs')
)


def initialization(self):
    self.addLink(None, "modality", self.update_modality)
    self.addLink(None, "noise_estimate", self.updateSignatureAboutNoise)
    self.addLink(None, "save_MPA", self.updateSignatureAboutMPA)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutMPA)
    self.addLink(None, "save_jacobians", self.updateSignatureAboutJacobians)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutJacobians)
    self.addLink(None, "save_divergences", self.updateSignatureAboutDivergences)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutDivergences)
    self.addLink(None, "save_deformation_fields", self.updateSignatureAboutDeformationField)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutDeformationField)
    self.addLink('MPA', 'volumes', self.update_MPA)
    self.addLink('jacobians', 'volumes',
                 lambda x: self.update_outputs(x, 'jacobians'))
    self.addLink('divergences', 'volumes',
                 lambda x: self.update_outputs(x, 'divergences'))
    self.addLink('deformation_fields', 'volumes',
                 lambda x: self.update_outputs(x, 'deformation_fields'))
    self.addLink('batch_location', 'volumes', self.updateBatchPath)

    # SPM default initialisation
    self.warping_regularisation = [0, 0, 100, 25, 100]
    self.bias_regularisation = 1000000
    self.save_MPA = True
    self.save_jacobians = False
    self.save_divergences = True
    self.save_deformation_fields = False


def update_modality(self, proc):
    self.signature['volumes'] = ListOf(ReadDiskItem(self.modality[0], ['NIFTI-1 image', 'SPM image', 'MINC image']))
    self.signature['MPA'] = WriteDiskItem(self.modality[1],
                                          ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                          requiredAttributes={'processing': 'spm12Serial'})
    self.changeSignature(self.signature)


def updateSignatureAboutNoise(self, proc):
    if self.noise_estimate == "NaN":
        self.setDisable("noise_estimate_value")
    elif self.noise_estimate in ["Scalar", "Matrix"]:
        self.setEnable("noise_estimate_value")
    else:
        raise ValueError("Unvalid noise_estimate")
    self.changeSignature(self.signature)


def updateSignatureAboutMPA(self, proc):
    if self.save_MPA and self.customs_outputs:
        self.setEnable("MPA")
    else:
        self.setDisable("MPA")
    self.changeSignature(self.signature)


def updateSignatureAboutJacobians(self, proc):
    if self.save_jacobians and self.customs_outputs:
        self.setEnable("jacobians")
    else:
        self.setDisable("jacobians")
    self.changeSignature(self.signature)


def updateSignatureAboutDivergences(self, proc):
    if self.save_divergences and self.customs_outputs:
        self.setEnable("divergences")
    else:
        self.setDisable("divergences")
    self.changeSignature(self.signature)


def updateSignatureAboutDeformationField(self, proc):
    if self.save_deformation_fields and self.customs_outputs:
        self.setEnable("deformation_fields")
    else:
        self.setDisable("deformation_fields")
    self.changeSignature(self.signature)


def update_MPA(self, proc):
    if self.volumes:
        attr = self.volumes[0].hierarchyAttributes()
        if 'name_serie' in attr.keys():
                del attr['name_serie']
        if attr:
            acquisitions = sorted([a.get('acquisition') for a in self.volumes])
            del attr['acquisition']
            del attr['normalized']
            attr['analysis'] = attr['modality'] + '_default_analysis'
            attr['acquisition_sequence'] = '_'.join(acquisitions)
            attr['space'] = 'average'
            return self.signature['MPA'].findValue(attr)


def update_outputs(self, proc, param):
    if self.volumes:
        attr = self.volumes[0].hierarchyAttributes()
        if 'name_serie' in attr.keys():
                del attr['name_serie']
        if attr:
            acquisitions = sorted([a.get('acquisition') for a in self.volumes])
            del attr['normalized']
            attr['analysis'] = attr['modality'] + '_default_analysis'
            del attr['modality']
            attr['acquisition_sequence'] = '_'.join(acquisitions)
            attr['space'] = 'average'
            param_list = []
            for vol in self.volumes:
                attr['acquisition'] = vol.get('acquisition')
                param_list.append(self.signature[param].contentType.findValue(attr))
            return param_list


def updateBatchPath(self, proc):
    if self.volumes:
        directory_path = os.path.dirname(self.volumes[0].fullPath())
        return os.path.join(directory_path, 'spm12_serial_job.m')


def execution(self, context):
    context.runProcess('SPM12Serial_generic',
                       volumes=self.volumes,
                       times=self.times,
                       noise_estimate=self.noise_estimate,
                       noise_estimate_value=self.noise_estimate_value,
                       warping_regularisation=self.warping_regularisation,
                       bias_regularisation=self.bias_regularisation,
                       customs_outputs=self.customs_outputs,
                       save_MPA=self.save_MPA,
                       MPA=self.MPA,
                       save_jacobians=self.save_jacobians,
                       jacobians=self.jacobians,
                       save_divergences=self.save_divergences,
                       divergences=self.divergences,
                       save_deformation_fields=self.save_deformation_fields,
                       deformation_fields=self.deformation_fields,
                       batch_location=self.batch_location)
