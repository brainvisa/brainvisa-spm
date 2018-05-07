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
import json

name = 'compute Grey / White / CSF / Skull / Scalp Mask'
userLevel = 0

signature=Signature(
    'grey_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'grey',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'}),
    'white_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'white',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'}),
    'csf_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'csf',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'}),
    'skull_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'skull',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'}),
    'scalp_native', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'scalp',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'}),
    'method', Choice(('threshold', 'threshold'),
                     ('max probability', 'maxProbability')),
    'threshold', Float(),
    'grey_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'grey'}),
    'white_mask', Boolean(),
    'white_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'white'}),
    'csf_mask', Boolean(),
    'csf_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'csf'}),
    #'intracranial_labels', Boolean(),
    #'intracranial_native_labels',
    #WriteDiskItem('T1 MRI intracranial labels',
                    #'NIFTI-1 image',
                    #requiredAttributes={'space':'t1mri'}),
    #'intracranial_native_translation',
    #WriteDiskItem('T1 MRI intracranial labels translation',
                    #'JSON file',
                    #requiredAttributes={'space':'t1mri'}),
    'skull_mask', Boolean(),
    'skull_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'skull'}),
    'scalp_mask', Boolean(),
    'scalp_native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'tissue_class':'scalp'}),
    'resolve_equal_proba', Boolean(),
)


def initialization( self ):
    self.setOptional('white_native', 'csf_native',
                     'skull_native', 'scalp_native',
                     'white_native_mask', 'csf_native_mask',
                     'skull_native_mask', 'scalp_native_mask')

    self.linkParameters('white_native', 'grey_native')
    self.linkParameters('csf_native', 'grey_native')
    self.linkParameters('skull_native', 'grey_native')
    self.linkParameters('scalp_native', 'grey_native')

    self.linkParameters("white_native_mask", "grey_native_mask")
    self.linkParameters("csf_native_mask", "grey_native_mask")
    self.linkParameters("skull_native_mask", "grey_native_mask")
    self.linkParameters("scalp_native_mask", "grey_native_mask")
    #self.linkParameters("intracranial_native_labels", "grey_native_mask")
    #self.linkParameters("intracranial_native_translation", "grey_native_mask")

    self.threshold = 0.2 # Chetelat G, Desgranges B, Landeau B, Mezenge F, Poline JB, de la Sayette V, et al. Direct voxel- based comparison between grey matter hypometabolism and atrophy in Alzheimer's disease. Brain 2008; 131: 60-71.
    self.method = 'maxProbability'
    self.white_mask=True
    self.csf_mask=True
    self.skull_mask=False
    self.scalp_mask=False
    #self.intracranial_labels=True


def execution( self, context ):
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
    #if (self.csf_mask or self.intracranial_labels or self.skull_mask or self.scalp_mask):
        #context.warning("only grey and white masks can be computed with threshold method.")
    else:
        self.compareProbabilityMapToList(self.grey_native, self.grey_native_mask, [self.white_native, self.csf_native, self.skull_native, self.scalp_native ])
        if (self.white_mask):
            self.compareProbabilityMapToList(self.white_native, self.white_native_mask, [self.grey_native, self.csf_native, self.skull_native, self.scalp_native ])
        if (self.csf_mask):
            self.compareProbabilityMapToList(self.csf_native, self.csf_native_mask, [self.grey_native, self.white_native, self.skull_native, self.scalp_native])
        if (self.skull_mask):
            self.compareProbabilityMapToList(self.skull_native, self.skull_native_mask, [self.grey_native, self.white_native, self.skull_native, self.scalp_native])
        if (self.scalp_mask):
            self.compareProbabilityMapToList(self.scalp_native, self.scalp_native_mask, [self.grey_native, self.white_native, self.skull_native, self.scalp_native])
        #if self.intracranial_labels:
            #self.createIntracranialLabel(context)


#def createIntracranialLabel(self, context):
  #volume = aims.read(self.grey_native_mask.fullPath())
  #array = np.array(volume, copy=False)
  #white_volume = aims.read(self.white_native_mask.fullPath())
  #white_array = np.array(white_volume, copy=False)
  #white_array *= 2
  #csf_volume = aims.read(self.csf_native_mask.fullPath())
  #csf_array = np.array(csf_volume, copy=False)
  #csf_array *= 3

  #array += white_array
  #if array.max() == 3:
      #context.warning("grey and white overlaps, the voxels will be set to 0")
      #array[array == 3] = 0
  #else:
    #pass

  #array += csf_array
  #if array.max() == 4:
      #context.warning("grey and csf overlaps, the voxels will be set to 0")
      #array[array == 4] = 0
  #elif array.max() == 5:
      #context.warning("white and csf overlaps, the voxels will be set to 0")
      #array[array == 5] = 0
  #else:
    #pass
  #aims.write(volume, self.intracranial_native_labels.fullPath())

  #data = {'1':'grey', '2':'white', '3':'csf'}
  #f = open(self.intracranial_native_translation.fullPath(), 'w')
  #json.dump(data, f, indent=2)
  #f.close()


def compareProbabilityMapToList(self, probabilityMap, mask, probMapsToCompare):
    """Function to create a mask from probability maps of different regions
    
    Compare the probabilityMap to all the other probability maps in probMapsToCompare
    If a probability is higher than in probabilityMap, the value in the mask is 0, else it's 1
    Create a file with the mask in mask.fullPath()
    
    Parameters
    ----------
    probabilityMap : 
        Probability map of the region to create a mask
    mask :
        Picture of the mask to be created
    probMapsToCompare : list
        List of all the others probability maps
    """

    volume = aims.read(probabilityMap.fullPath())
    array = np.array(volume, copy=False)
    array[np.where(array < 0)] = 0
    for probToCompare in probMapsToCompare:
        self.compareProbabilityMap(array, probToCompare)
    array[array > 10e-5] = 1  # 0 in nii.gz can be 4.65661e-10 in .nii after AimsFileConvert
    aims.write(volume, mask.fullPath(), format='S16')


def compareProbabilityMap(self, array, probMap):
    if probMap is None or not os.path.exists(probMap.fullPath()):
        return
    compArray = np.array(aims.read(probMap.fullPath()), copy=False)
    if self.resolve_equal_proba:
        if len(array.shape) == 4 and len(compArray.shape) == 4:
            array = resolveEqualProbability(array, compArray)
        else:
            raise ValueError('this code is only implemented for 4D shape')
    else:
        pass
    array[array < compArray] = 0


def resolveEqualProbability(arr, comp_arr):
    equal_arr = arr == comp_arr
    empty_arr = arr.copy()
    empty_arr.fill(0)
    non_zero_array = arr != empty_arr  # to remove voxel equal to 0.0
    equal_coord = np.where(equal_arr * non_zero_array)
    for x, y, z, t in zip(equal_coord[0], equal_coord[1], equal_coord[2], equal_coord[3]):
        if 0 < x < arr.shape[0] and 0 < y < arr.shape[1] and 0 < z < arr.shape[2] and 0 < t < arr.shape[3] :
            neighbors_arr_mean = _computeNeighborsMean(arr, x, y, z, t)
            neighbors_comp_arr_mean = _computeNeighborsMean(comp_arr, x, y, z, t)
            if neighbors_arr_mean < neighbors_comp_arr_mean:
                arr[x][y][z][t] = 0
        else:
            pass  # voxel neighbor is out of field of view
    return arr


def _computeNeighborsMean(arr, x, y, z, t):
    "18 neighbors"
    neighbors_6 = [[x-1, y, z, t],
                   [x, y-1, z, t],
                   [x, y, z-1, t],
                   [x+1, y, z, t],
                   [x, y+1, z, t],
                   [x, y, z+1, t],
                  ]
    neighbors_18 = neighbors_6 +\
                   [[x-1, y-1, z, t],
                    [x, y-1, z-1, t],
                    [x-1, y, z-1, t],
                    [x+1, y+1, z, t],
                    [x, y+1, z+1, t],
                    [x+1, y, z+1, t],
                   ]
    neighbors_sum = 0
    for n in neighbors_18:
        neighbors_sum += arr[n[0]][n[1]][n[2]][n[3]]
    return neighbors_sum / len(neighbors_18)
