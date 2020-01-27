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

name = 'compute one tissue mask'
userLevel = 1

signature = Signature(
    'native_prob_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
    'others_prob_maps', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'])),

    'native_mask', WriteDiskItem(
        'T1 MRI tissue probability mask',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
    'resolve_equal_probability', Boolean()

)


def initialization(self):
    #self.linkParameters('others_prob_maps', 'native_prob_map')  # TODO Test and take only others map differents from native_map_prob
    self.resolve_equal_probability = True


def execution(self, context):

    print("Compute one tissue mask")
    prob_map_vol = aims.read(self.native_prob_map.fullPath())
    prob_map_arr = np.array(prob_map_vol, copy=False)
    prob_map_arr[prob_map_arr < 0] = 0
    
    comp_prob_map_max = []
    for other_prob_map in self.others_prob_maps:
        # comp_prob_map_arr = np.array(aims.read(other_prob_map.fullPath()), copy=False)
        comp_prob_map_max.append(np.array(aims.read(other_prob_map.fullPath()), copy=False))
        # self.compare_probability_map(prob_map_arr, comp_prob_map_arr)
    comp_prob_map_arr = np.max(comp_prob_map_max, axis=0)
    self.compare_probability_map(prob_map_arr, comp_prob_map_arr)

    prob_map_arr[prob_map_arr > 10e-5] = 1
    aims.write(prob_map_vol, self.native_mask.fullPath(), format='S16')


def compare_probability_map(self, prob_map, comp_prob_map):

    if self.resolve_equal_probability:
        self._resolve_equal_probability(prob_map, comp_prob_map)
        
    prob_map[prob_map < comp_prob_map] = 0


def _resolve_equal_probability(self, prob_map, comp_prob_map):
    """ Function to resolve all the equal voxel between prob_map and comp_prob_map

    For each voxel with the same value, compute the mean value off the 18 neighbors of the pixels
    and keep the mask for the higher mean.
    """

    if len(prob_map.shape) == 4 and len(comp_prob_map.shape) == 4:
        equal_arr = prob_map == comp_prob_map
        empty_arr = np.zeros(prob_map.shape)
        non_zero_array = prob_map != empty_arr  # Replace by np.where != 0 ?
        equal_coord = np.where(equal_arr * non_zero_array)
        for x, y, z, t in zip(equal_coord[0], equal_coord[1], equal_coord[2], equal_coord[3]):
            if 0 <= x < prob_map.shape[0] and 0 <= y < prob_map.shape[1] and 0 <= z < prob_map.shape[2] and 0 <= t < prob_map.shape[3]:
                neighbors_arr_mean = _computeNeighborsMean(prob_map, x, y, z, t)
                neighbors_comp_arr_mean = _computeNeighborsMean(comp_prob_map, x, y, z, t)
                if neighbors_arr_mean < neighbors_comp_arr_mean:
                    prob_map[x][y][z][t] = 0
                else:
                    prob_map[x][y][z][t] = 1
            else:
                pass  # voxel neighbors is out of field of view

    else:
        raise ValueError('This code is only implemented for 4D shape')


def _computeNeighborsMean(arr, x, y, z, t):
    """Compute the mean value of the 18 neighbors"""

    neighbors_6 = [
        [x - 1, y, z, t],
        [x, y - 1, z, t],
        [x, y, z - 1, t],
        [x + 1, y, z, t],
        [x, y + 1, z, t],
        [x, y, z + 1, t],
    ]
    neighbors_18 = neighbors_6 + [
        [x - 1, y - 1, z, t],
        [x, y - 1, z - 1, t],
        [x - 1, y, z - 1, t],
        [x + 1, y + 1, z, t],
        [x, y + 1, z + 1, t],
        [x + 1, y, z + 1, t],
        [x - 1, y + 1, z, t],
        [x, y - 1, z + 1, t],
        [x - 1, y, z + 1, t],
        [x + 1, y - 1, z, t],
        [x, y + 1, z - 1, t],
        [x + 1, y, z - 1, t]
    ]
    
    neighbors_sum = 0
    for n in neighbors_18:
        neighbors_sum += arr[n[0]][n[1]][n[2]][n[3]]
    return neighbors_sum / len(neighbors_18)
