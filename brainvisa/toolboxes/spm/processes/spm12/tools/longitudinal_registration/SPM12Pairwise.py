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
from soma.spm.spm12.tools.longitudinal_registration.pairwise import PairwiseLongitudinalRegistration
from soma.spm.spm_launcher import SPM12, SPM12Standalone

configuration = Application().configuration


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


userLevel = 0
name = 'spm12 - Pairwise longitudinal registration'


signature = Signature(
    'modality', Choice(('T1 MRI', 'Raw T1 MRI'),
                       ('FLAIR MRI', 'Raw FLAIR MRI')),
    'time_1_volumes', ListOf(ReadDiskItem('Raw T1 MRI', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    'time_2_volumes', ListOf(ReadDiskItem('Raw T1 MRI', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
    'time_difference', ListOf(Float()),
    'noise_estimate', Choice("NaN", "Scalar", "Matrix"),
    'noise_estimate_value', Matrix(),
    'warping_regularisation', ListOf(Float()),
    'bias_regularisation', Float(),
    'customs_outputs', Boolean(),
    'save_MPA', Boolean(),
    'MPA', ListOf(WriteDiskItem('T1 MRI mid-point average', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                requiredAttributes={'processing': 'spm12Pairwise'})),
    'save_jacobian_rate', Boolean(),
    'jacobian_rate', ListOf(WriteDiskItem('Jacobian determinant', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                          requiredAttributes={'processing': 'spm12Pairwise'})),
    'save_divergence_rate', Boolean(),
    'divergence_rate', ListOf(WriteDiskItem('Divergence map', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                            requiredAttributes={'processing': 'spm12Pairwise'})),
    'save_deformation_fields', Boolean(),
    'time_1_deformation_fields', ListOf(WriteDiskItem('SPM deformation field', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                                      requiredAttributes={'processing': 'spm12Pairwise',
                                                                          'orientation': 'baseline_to_halfway'})),
    'time_2_deformation_fields', ListOf(WriteDiskItem('SPM deformation field', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                                      requiredAttributes={'processing': 'spm12Pairwise',
                                                                          'orientation': 'followup_to_halfway'})),
    'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', section='default SPM outputs')
)


def initialization(self):
    self.addLink(None, "noise_estimate", self.updateSignatureAboutNoise)
    self.addLink(None, "save_MPA", self.updateSignatureAboutMPA)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutMPA)
    self.addLink(None, "save_jacobian_rate", self.updateSignatureAboutJacobianRate)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutJacobianRate)
    self.addLink(None, "save_divergence_rate", self.updateSignatureAboutDivergenceRate)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutDivergenceRate)
    self.addLink(None, "save_deformation_fields", self.updateSignatureAboutDeformationField)
    self.addLink(None, "customs_outputs", self.updateSignatureAboutDeformationField)
    self.addLink("batch_location", "time_1_volumes", self.updateBatchPath)
    
    self.addLink(None, ("time_1_volumes", "time_2_volumes"), self.update_outputs)
    self.addLink(None, "modality", self.update_modality)

    # SPM default initialisation
    self.time_difference = [1]
    self.noise_estimate = "NaN"
    self.warping_regularisation = [0, 0, 100, 25, 100]
    self.bias_regularisation = 1000000
    self.save_MPA = True
    self.save_jacobian_rate = False
    self.save_divergence_rate = True
    self.save_deformation_fields = False


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


def updateSignatureAboutJacobianRate(self, proc):
    if self.save_jacobian_rate and self.customs_outputs:
        self.setEnable("jacobian_rate")
    else:
        self.setDisable("jacobian_rate")
    self.changeSignature(self.signature)


def updateSignatureAboutDivergenceRate(self, proc):
    if self.save_divergence_rate and self.customs_outputs:
        self.setEnable("divergence_rate")
    else:
        self.setDisable("divergence_rate")
    self.changeSignature(self.signature)


def updateSignatureAboutDeformationField(self, proc):
    if self.save_deformation_fields and self.customs_outputs:
        self.setEnable("time_1_deformation_fields",
                       "time_2_deformation_fields")
    else:
        self.setDisable("time_1_deformation_fields",
                        "time_2_deformation_fields")
    self.changeSignature(self.signature)


def updateBatchPath(self, proc):
    if self.time_1_volumes:
        directory_path = os.path.dirname(self.time_1_volumes[0].fullPath())
        return os.path.join(directory_path, 'spm12_pairwaise_job.m')


def update_modality(self, proc):
    self.signature['time_1_volumes'] = ListOf(ReadDiskItem(self.modality, ['NIFTI-1 image', 'SPM image', 'MINC image']))
    self.signature['time_2_volumes'] = ListOf(ReadDiskItem(self.modality, ['NIFTI-1 image', 'SPM image', 'MINC image']))
    self.changeSignature(self.signature)


def update_outputs(self, *proc):
    mpa_list = []
    jacobian_list = []
    divergence_list = []
    deformation1_list = []
    deformation2_list = []
    
    if self.time_1_volumes and self.time_2_volumes and len(self.time_1_volumes) == len(self.time_2_volumes):
        for time_1_vol, time_2_vol in zip(self.time_1_volumes, self.time_2_volumes):
            attr = time_1_vol.hierarchyAttributes()
            attr['baseline'] = attr.pop('acquisition')
            attr_2 = time_2_vol.hierarchyAttributes()
            attr['followup'] = attr_2['acquisition']
            
            attr['analysis'] = attr['modality']
            
            mpa_list.append(self.signature['MPA'].contentType.findValue(attr))
            jacobian_list.append(self.signature['jacobian_rate'].contentType.findValue(attr))
            divergence_list.append(self.signature['divergence_rate'].contentType.findValue(attr))
            deformation1_list.append(self.signature['time_1_deformation_fields'].contentType.findValue(attr))
            deformation2_list.append(self.signature['time_2_deformation_fields'].contentType.findValue(attr))
            
    self.MPA = mpa_list
    self.jacobian_rate = jacobian_list
    self.divergence_rate = divergence_list
    self.time_1_deformation_fields = deformation1_list
    self.time_2_deformation_fields = deformation2_list


def execution(self, context):
    if len(self.time_1_volumes) != len(self.time_2_volumes):
        context.error('time_1_volumes and time_2_volumes have to be the same length!')
    else:
        context.runProcess('SPM12Pairwise_generic',
                           time_1_volumes=self.time_1_volumes,
                           time_2_volumes=self.time_2_volumes,
                           time_difference=self.time_difference,
                           noise_estimate=self.noise_estimate,
                           noise_estimate_value=self.noise_estimate_value,
                           warping_regularisation=self.warping_regularisation,
                           bias_regularisation=self.bias_regularisation,
                           customs_outputs=self.customs_outputs,
                           save_MPA=self.save_MPA,
                           MPA=self.MPA,
                           save_jacobian_rate=self.save_jacobian_rate,
                           jacobian_rate=self.jacobian_rate,
                           save_divergence_rate=self.save_divergence_rate,
                           divergence_rate=self.divergence_rate,
                           save_deformation_fields=self.save_deformation_fields,
                           time_1_deformation_fields=self.time_1_deformation_fields,
                           time_2_deformation_fields=self.time_2_deformation_fields,
                           batch_location=self.batch_location)
