# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 18:28:35 2021

@author: urielle.thoprakarn
"""

import numpy as np
import math

from soma import aims

def getSpmImagesListFrom4DVolume(input_4D_image_path):
    """Create SPM-compatible images list from 4D volume."""
    nsteps = get_number_of_time_steps(input_4D_image_path)
    images_path_list = [input_4D_image_path + ',' + str(n) 
                        for n in range(1, nsteps + 1)]
    return images_path_list
        
        
def get_number_of_time_steps(image_4D_path):
    """Return number of time steps in 4D volume."""
    input_array = np.array(aims.read(image_4D_path), copy=False)
    if len(input_array.shape) != 4 or input_array.shape[-1] == 1:
        raise RuntimeError('Image is not in 4D.')
    
    return input_array.shape[-1]
    
    
def get_tr(image_path):
    """Return TR from image's header."""
    volume = aims.read(image_path)
    if 'tr' not in volume.header().keys():
        raise KeyError('TR not found.')
    
    tr = volume.header()['tr']
    if tr == 0 or tr == 1:
        raise ValueError('Suspicious TR value in NIFTI header: ' + str(tr))
    
    return tr


def get_slice_order(nb_slices, order, scanner):
    """ 
    Returns slice order for SPM slice timing correction
    ---------------------------------------------------

    Scanner modes and subsequent slice orders were found on:
    https://en.wikibooks.org/wiki/SPM/Slice_Timing

    For SIEMENS and interleaved slice order, if the number of slices is even
    slice order will be 2 4 6 1 3 5, and 1 3 5 2 4 6 if it is uneven : see
    https://practicalfmri.blogspot.com/2012/07/siemens-slice-ordering.html

    Parameters
    ----------
    nb_slices: int
        number of slices in one fmri volume.
    order: str
        slice order. Can be :
            - For SIEMENS : Ascending sequential, Ascending sequential
                            reversed, Descending sequential,
                            Descending sequential reversed,
                            Ascending interleaved,
                            Ascending interleaved reversed (Descending)
            - For PHILIPS : Default Single package, Default Two packages,
                            Default Multi-packages (>2), Ascending Single
                            package, Ascending Multi-packages, Decending
                            Single package, Decending Multi-packages,
                            Central Single package?,
                            Reverse Central Single package?,
                            Interleaved Single package?
    scanner: str
        scanner.

    Returns:
    --------
    slices_order: array of int
        slices order array.
    """
    slices_order = []

    if scanner.upper() == "SIEMENS":
        if order == "Ascending sequential":
            slices_order = [x for x in range(1, nb_slices + 1)]
        elif order == "Descending sequential":
            slices_order = [x for x in range(nb_slices, 0, -1)]

        # Even first
        elif order == "Ascending interleaved" and nb_slices % 2 == 0:
            slices_order.extend(
                [x for x in range(2, nb_slices + 1, 2)])
            slices_order.extend(
                [x for x in range(1, nb_slices + 1, 2)])

        # Odd-first
        elif order == "Ascending interleaved" and nb_slices % 2 != 0:
            slices_order.extend(
                [x for x in range(1, nb_slices + 1, 2)])
            slices_order.extend(
                [x for x in range(2, nb_slices + 1, 2)])
        elif order in [
            "Ascending sequential reversed", "Descending sequential reversed",
                "Ascending interleaved reversed"]:
            # TODO: There is a difference between SIEMENS Magnetom machines and
            # other machines for reversed sequences (see SPM wiki).
            # To be implemented later
            raise NotImplementedError(
                "Case for SIEMENS scanner and reversed sequences has not been "
                "implemented yet.")
        else:
            raise NotImplementedError(
                "Unknown sequence for SIEMENS '{0}'".format(order))
    elif scanner.upper() == "PHILIPS":
        if order == "Interleaved Single package?":
            # NOTE : For Interleaved Single Package? sequence, the slice order
            # begins to one and is spaced with an increment that is the root
            # square of the number of slices
            increment = math.sqrt(nb_slices)
            increment = math.ceil(increment)
            for idx in range(1, nb_slices + 1):
                if idx not in slices_order:
                    slices_order.extend(
                        [x for x in range(idx, nb_slices + 1, increment)])
        elif order in (
            "Default Single package", "Default Two packages",
            "Default Multi-packages (>2)", "Ascending Single package",
            "Ascending Multi-packages", " Decending Single package",
            "Decending Multi-packages", "Central Single package?",
                "Central Single package?", "Reverse Central Single package?"):
            raise NotImplementedError(
                "Lazy developper has not implemented yet sequence '{0}' for "
                "scanner PHILIPS".format(order))
    else:
        raise NotImplementedError(
            "No case implemented for scanner '{0}', only for SIEMENS and "
            "PHILIPS.".format(scanner))
    return slices_order


def st_get_ref_slice(ref_slice, slice_order):
    """ 
    Returns slice index for slice timing correction reference slice.
    ----------------------------------------------------------------

    Returns 'First', 'Middle', or 'Last' slice index based on slice order.

    Parameters
    ----------
    ref_slice: str
        Indicates if user wants to use first, middle (temporal) or last slice
        for slice timing correction.
    slice_order: int array
        slice order.

    Returns:
    --------
    ref_slice_idx: int
        Reference slice index.
    """

    if ref_slice == "First":
        ref_slice_idx = slice_order[0]
    elif ref_slice == "Last":
        ref_slice_idx = slice_order[-1]
    elif ref_slice == "Middle":
        if len(slice_order) % 2 == 0:
            ref_slice_idx = slice_order[int(len(slice_order) / 2) - 1]
        else:
            ref_slice_idx = slice_order[math.floor(len(slice_order) / 2)]
    else:
        raise ValueError("Ref slice must be either First, Middle or Last."
                         " Not : {0}.".format(ref_slice))
    return ref_slice_idx
