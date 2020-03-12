# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
#      Equipe Cogimage
#      UPMC, CRICM, UMR-S975
#      CNRS, UMR 7225
#      INSERM, U975
#      Hopital Pitie Salpetriere
#      47 boulevard de l'Hopital
#      75651 Paris cedex 13
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

from brainvisa.processes import *
import numpy as np

name = 'compute Grey / White / CSF / Skull / Scalp Mask'
userLevel = 0

signature=Signature(
    'grey_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'grey',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'white_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'white',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'csf_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'csf',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'skull_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'skull',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'scalp_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'scalp',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'background_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'background',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'method', Choice(('threshold', 'threshold'),
                     ('max probability', 'maxProbability')),
    'threshold', Float(),
    'grey_mask', Boolean(),
    'grey_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'grey'}),
    'white_mask', Boolean(),
    'white_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'white'}),
    'csf_mask', Boolean(),
    'csf_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'csf'}),
    'intracranial_labels', Boolean(),
    'intracranial_native_labels',
    WriteDiskItem('T1 MRI intracranial labels',
                    'NIFTI-1 image',
                    requiredAttributes={'space': 't1mri'}),
    'intracranial_native_translation',
    WriteDiskItem('T1 MRI intracranial labels translation',
                    'JSON file',
                    requiredAttributes={'space': 't1mri'}),
    'skull_mask', Boolean(),
    'skull_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'skull'}),
    'scalp_mask', Boolean(),
    'scalp_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'scalp'}),
    'background_mask', Boolean(),
    'background_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class': 'background'}),
    'resolve_equal_proba', Boolean(),
)


def initialization(self):
    self.setOptional('grey_native_mask', 'white_native', 'csf_native',
                     'skull_native', 'scalp_native', 'background_native'
                     'white_native_mask', 'csf_native_mask',
                     'skull_native_mask', 'scalp_native_mask',
                     'background_native_mask')

    self.linkParameters('white_native', 'grey_native')
    self.linkParameters('csf_native', 'grey_native')
    self.linkParameters('skull_native', 'grey_native')
    self.linkParameters('scalp_native', 'grey_native')
    self.linkParameters('background_native', 'grey_native')

    self.linkParameters("white_native_mask", "grey_native_mask")
    self.linkParameters("csf_native_mask", "grey_native_mask")
    self.linkParameters("skull_native_mask", "grey_native_mask")
    self.linkParameters("scalp_native_mask", "grey_native_mask")
    self.linkParameters("background_native_mask", "grey_native_mask")
    self.linkParameters("intracranial_native_labels", "grey_native_mask")
    self.linkParameters("intracranial_native_translation", "grey_native_mask")
    
    self.linkParameters(None, 'intracranial_labels', self._update_icl)

    self.threshold = 0.2 # Chetelat G, Desgranges B, Landeau B, Mezenge F, Poline JB, de la Sayette V, et al. Direct voxel- based comparison between grey matter hypometabolism and atrophy in Alzheimer's disease. Brain 2008; 131: 60-71.
    self.method = 'maxProbability'
    self.white_mask = True
    self.csf_mask = True
    self.skull_mask = False
    self.scalp_mask = False
    self.intracranial_labels = True


def execution(self, context):
    if(self.method == 'threshold'):
        context.system('AimsThreshold',
                       '-i', self.grey_native.fullPath(),
                       '-o', self.grey_native_mask.fullPath(),
                       '-t', self.threshold,
                       '--fg', 1,
                       '-m', 'gt', '-b')
        if (self.white_mask):
            context.system('AimsThreshold',
                           '-i', self.white_native.fullPath(),
                           '-o', self.white_native_mask.fullPath(),
                           '-t', self.threshold,
                           '--fg', 1,
                           '-m', 'gt', '-b')
        if (self.csf_mask or self.intracranial_labels or self.skull_mask or self.scalp_mask):
            context.warning("only grey and white masks can be computed with threshold method.")
    else:
        if (self.grey_mask):
            self.compareProbabilityMapToList(context, self.grey_native, self.grey_native_mask, [self.white_native, self.csf_native, self.skull_native, self.scalp_native, self.background_native])
        if (self.white_mask):
            self.compareProbabilityMapToList(context, self.white_native, self.white_native_mask, [self.grey_native, self.csf_native, self.skull_native, self.scalp_native, self.background_native])
        if (self.csf_mask):
            self.compareProbabilityMapToList(context, self.csf_native, self.csf_native_mask, [self.grey_native, self.white_native, self.skull_native, self.scalp_native, self.background_native])
        if (self.skull_mask):
            self.compareProbabilityMapToList(context, self.skull_native, self.skull_native_mask, [self.grey_native, self.white_native, self.csf_native, self.scalp_native, self.background_native])
        if (self.scalp_mask):
            self.compareProbabilityMapToList(context, self.scalp_native, self.scalp_native_mask, [self.grey_native, self.white_native, self.csf_native, self.skull_native, self.background_native])
        if (self.background_mask):
            self.compareProbabilityMapToList(context, self.scalp_native, self.scalp_native_mask, [self.grey_native, self.white_native, self.csf_native, self.skull_native, self.scalp_native])
        if self.intracranial_labels:
            self.createIntracranialLabel(context)


def createIntracranialLabel(self, context):
    volume = aims.read(self.grey_native_mask.fullPath())
    array = np.array(volume, copy=False)
    white_volume = aims.read(self.white_native_mask.fullPath())
    white_array = np.array(white_volume, copy=False)
    white_array *= 2
    csf_volume = aims.read(self.csf_native_mask.fullPath())
    csf_array = np.array(csf_volume, copy=False)
    csf_array *= 3

    array += white_array
    if array.max() == 3:
        context.warning("grey and white overlaps, the voxels will be set to 0")
        array[array == 3] = 0
    else:
        pass

    array += csf_array
    if array.max() == 4:
        context.warning("grey and csf overlaps, the voxels will be set to 0")
        array[array == 4] = 0
    elif array.max() == 5:
        context.warning("white and csf overlaps, the voxels will be set to 0")
        context.warning(np.where(array == 5))
        array[array == 5] = 0
    else:
        pass
    aims.write(volume, self.intracranial_native_labels.fullPath())

    data = {'1': 'grey', '2': 'white', '3': 'csf'}
    f = open(self.intracranial_native_translation.fullPath(), 'w')
    json.dump(data, f, indent=2)
    f.close()


def compareProbabilityMapToList(self, context, prob_map, prob_map_output, prob_maps_to_compare):
    """Function to create a mask from probability maps of different regions

    Compare the probabilityMap to all the other probability maps in probMapsToCompare
    If a probability is higher than in probabilityMap, the value in the mask is 0, else it's 1
    Create a file with the mask in mask.fullPath()
    """

    compute_one = getProcessInstance('computeOneTissueMask')
    compute_one.native_prob_map = prob_map.fullPath()
    compute_one.others_prob_maps = [i.fullPath() for i in prob_maps_to_compare if i]
    compute_one.native_mask = prob_map_output.fullPath()
    context.runProcess(compute_one)


def _update_icl(self, *sources):
    if self.intracranial_labels:
        self.setEnable('intracranial_native_labels', 'intracranial_native_translation')
    else:
        self.setDisable('intracranial_native_labels', 'intracranial_native_translation')
    self.changeSignature(self.signature)
