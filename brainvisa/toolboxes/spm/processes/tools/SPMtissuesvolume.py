# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *
from soma import aims
import numpy as np


name = 'SPM - Brain Tissues Volumes'
userLevel = 0

signature = Signature(
    'white_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'white',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'})),
    'white_warped_unmodulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'white',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'low-dimensional'})),
    'white_warped_modulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'white',
                            'transformation':'none',
                            'modulation':'affine and non-linear',
                            'warping_method':'low-dimensional'})),
    'grey_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'grey',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'})),
    'grey_warped_unmodulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'grey',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'low-dimensional'})),
    'grey_warped_modulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'grey',
                            'transformation':'none',
                            'modulation':'affine and non-linear',
                            'warping_method':'low-dimensional'})),
    'csf_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'csf',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'})),
    'csf_warped_unmodulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'csf',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'low-dimensional'})),
    'csf_warped_modulated_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'csf',
                            'transformation':'none',
                            'modulation':'affine and non-linear',
                            'warping_method':'low-dimensional'})),
    'skull_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'skull',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'})),
    'scalp_proba_map', ListOf(ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class':'scalp',
                            'transformation':'none',
                            'modulation':'none',
                            'warping_method':'none'})),
    'mode', Choice(('Sum of the wm images', 'default'),
                   ('Sum of the native images (VBM8)', 'native'),
                   ('Sum of the wm images + TIV mask (Malone)', 'default+mask'),
                   ('Sum of the wm images + individual TIV mask', 'default+ind_mask'),
                   ('Probability maximum', 'proba_max')),
    'tiv_mask', ReadDiskItem(
        'Label Volume',
        'Aims readable volume formats'),
    'tissues_volumes_file', WriteDiskItem('CSV File', 'CSV File')
)


def initialization(self):
    self.linkParameters('white_warped_unmodulated_proba_map', 'white_proba_map')
    self.linkParameters('white_warped_modulated_proba_map', 'white_proba_map')
    self.linkParameters('grey_proba_map', 'white_proba_map')
    self.linkParameters('grey_warped_unmodulated_proba_map', 'grey_proba_map')
    self.linkParameters('grey_warped_modulated_proba_map', 'grey_proba_map')
    self.linkParameters('csf_proba_map', 'grey_proba_map')
    self.linkParameters('csf_warped_unmodulated_proba_map', 'csf_proba_map')
    self.linkParameters('csf_warped_modulated_proba_map', 'csf_proba_map')
    self.linkParameters('skull_proba_map', 'csf_proba_map')
    self.linkParameters('scalp_proba_map', 'skull_proba_map')
    self.tissues_volumes_file = os.path.join(os.getcwd(), 'tissues_volumes_spm.csv')
    self.mode = 'default'
    self.setOptional('white_warped_unmodulated_proba_map')
    self.setOptional('grey_warped_unmodulated_proba_map')
    self.setOptional('csf_warped_unmodulated_proba_map')
    self.setOptional('skull_proba_map')
    self.setOptional('scalp_proba_map')
    self.setOptional('tiv_mask')
    


def execution(self, context):
    nb = len(self.white_proba_map)
    f = open(self.tissues_volumes_file.fullPath(), 'w')
    f.write('subject,grey,white,csf,tiv\n')
    
    for index, white_map in enumerate(self.white_proba_map):
        context.progress(index, nb, process=self)
        subject  = white_map.get('subject')
        
        if self.mode == 'default+ind_mask':
            #Compute an approximate intracranial mask from normalized images
            white_w = aims.read(self.white_warped_unmodulated_proba_map[index].fullPath())
            grey_w = aims.read(self.grey_warped_unmodulated_proba_map[index].fullPath())
            csf_w = aims.read(self.csf_warped_unmodulated_proba_map[index].fullPath())
            white_w_arr = white_w.arraydata()
            grey_w_arr = grey_w.arraydata()
            csf_w_arr = csf_w.arraydata()
            
            tiv_ind_arr = white_w_arr + grey_w_arr + csf_w_arr
            tiv_mask_ind_arr = (tiv_ind_arr > 0.5)

            tiv_mask = tiv_mask_ind_arr.astype('int16')
            tiv_mask_vol = aims.Volume_S16(tiv_mask)
            for key in white_w.header().keys():
                tiv_mask_vol.header()[key]=white_w.header()[key]
            tmpfile = context.temporary('gz compressed NIFTI-1 image')
            aims.write(tiv_mask_vol, tmpfile)
        
        elif self.mode == 'default+mask':
            tiv_mask = aims.read(self.tiv_mask.fullPath())
            tiv_mask_arr = tiv_mask.arraydata()
        
        if self.mode == 'default' or self.mode == 'default+mask' or self.mode == 'default+ind_mask':
            white_mw = aims.read(self.white_warped_modulated_proba_map[index].fullPath())
            grey_mw = aims.read(self.grey_warped_modulated_proba_map[index].fullPath())
            csf_mw = aims.read(self.csf_warped_modulated_proba_map[index].fullPath())
            white_mw_arr = white_mw.arraydata()
            grey_mw_arr = grey_mw.arraydata()
            csf_mw_arr = csf_mw.arraydata()
            white_mw_arr = white_mw_arr.astype('float64')
            grey_mw_arr = grey_mw_arr.astype('float64')
            csf_mw_arr = csf_mw_arr.astype('float64')
            tiv_mw_arr = white_mw_arr + grey_mw_arr + csf_mw_arr            
            
            if self.mode == 'default+mask':
                white_mw_arr[tiv_mask_arr == False] = 0.
                grey_mw_arr[tiv_mask_arr == False] = 0.
                csf_mw_arr[tiv_mask_arr == False] = 0.
                tiv_mw_arr[tiv_mask_arr == False] = 0.
            elif self.mode == 'default+ind_mask':
                white_mw_arr[tiv_mask_ind_arr == False] = 0.
                grey_mw_arr[tiv_mask_ind_arr == False] = 0.
                csf_mw_arr[tiv_mask_ind_arr == False] = 0.
                tiv_mw_arr[tiv_mask_ind_arr == False] = 0.
            
            white_mw_arr[white_mw_arr < 0] = 0.
            grey_mw_arr[grey_mw_arr < 0] = 0.
            csf_mw_arr[csf_mw_arr < 0] = 0.
            tiv_mw_arr[tiv_mw_arr < 0] = 0.

            white_mw_arr = white_mw_arr[~np.isnan(white_mw_arr)]
            grey_mw_arr = grey_mw_arr[~np.isnan(grey_mw_arr)]
            csf_mw_arr = csf_mw_arr[~np.isnan(csf_mw_arr)]
            tiv_mw_arr = tiv_mw_arr[~np.isnan(tiv_mw_arr)]

            vox_sizes = white_mw.header()['voxel_size']
            vox_vol = vox_sizes[0]*vox_sizes[1]*vox_sizes[2]       

            tiv_mw_arr_mm3 = tiv_mw_arr*vox_vol     
            white_mw_arr_mm3 = white_mw_arr*vox_vol
            grey_mw_arr_mm3 = grey_mw_arr*vox_vol
            csf_mw_arr_mm3 = csf_mw_arr*vox_vol
            
            tiv = tiv_mw_arr_mm3.sum()/1000.
            wm_vol = white_mw_arr_mm3.sum()/1000.
            gm_vol = grey_mw_arr_mm3.sum()/1000.
            csf_vol = csf_mw_arr_mm3.sum()/1000.
            
        elif self.mode == 'native':
            white = aims.read(self.white_proba_map[index].fullPath())
            grey = aims.read(self.grey_proba_map[index].fullPath())
            csf = aims.read(self.csf_proba_map[index].fullPath())
            white_arr = white.arraydata()
            grey_arr = grey.arraydata()
            csf_arr = csf.arraydata()
            white_arr = white_arr.astype('float64')
            grey_arr = grey_arr.astype('float64')
            csf_arr = csf_arr.astype('float64')            
            tiv_arr = white_arr + grey_arr + csf_arr
            
            vox_sizes = white.header()['voxel_size']
            vox_vol = vox_sizes[0]*vox_sizes[1]*vox_sizes[2]
            
            tiv_arr_mm3 = tiv_arr*vox_vol
            white_arr_mm3 = white_arr*vox_vol
            grey_arr_mm3 = grey_arr*vox_vol
            csf_arr_mm3 = csf_arr*vox_vol
            
            tiv = tiv_arr_mm3.sum()/1000.
            wm_vol = white_arr_mm3.sum()/1000.
            gm_vol = grey_arr_mm3.sum()/1000.
            csf_vol = csf_arr_mm3.sum()/1000.
              
        elif self.mode == 'proba_max':
            white = aims.read(self.white_proba_map[index].fullPath())
            grey = aims.read(self.grey_proba_map[index].fullPath())
            csf = aims.read(self.csf_proba_map[index].fullPath())
            skull = aims.read(self.skull_proba_map[index].fullPath())
            scalp = aims.read(self.scalp_proba_map[index].fullPath())
            white_arr = white.arraydata()
            grey_arr = grey.arraydata()
            csf_arr = csf.arraydata()
            skull_arr = skull.arraydata()
            scalp_arr = scalp.arraydata()
            white_arr = white_arr.astype('float64')
            grey_arr = grey_arr.astype('float64')
            csf_arr = csf_arr.astype('float64')
            skull_arr = skull_arr.astype('float64')
            scalp_arr = scalp_arr.astype('float64')
            
            vox_sizes = white.header()['voxel_size']
            vox_vol = vox_sizes[0]*vox_sizes[1]*vox_sizes[2]
            
            #Classify
            wm_arr = (white_arr > grey_arr) & (white_arr > csf_arr) & \
                     (white_arr > skull_arr) & (white_arr > scalp_arr)
            gm_arr = (grey_arr > white_arr) & (grey_arr > csf_arr) & \
                     (grey_arr > skull_arr) & (grey_arr > scalp_arr)
            csf_arr = (csf_arr > white_arr) & (csf_arr > grey_arr) & \
                      (csf_arr > skull_arr) & (csf_arr > scalp_arr)
            tiv_arr = wm | gm | csf
            
            ##Calculation of the volumes
            #wm_vol = wm_arr.sum()*vox_vol/1000.
            #gm_vol = gm_arr.sum()*vox_vol/1000.
            #csf_vol = csf_arr.sum()*vox_vol/1000.
            #tiv = tiv_arr.sum()*vox_vol/1000.
            
            #Creation of a mask of connected components (CCs) (26 connexity)
            tiv_arr = tiv_arr.astype('int16')
            tiv_mask = aims.Volume_S16(tiv_arr)
            for key in white.header().keys():
                tiv_mask.header()[key]=white.header()[key]
                tiv_mask.header()[key]=white.header()[key]
            tmpfile = context.temporary('gz compressed NIFTI-1 image')
            aims.write(tiv_mask, tmpfile)
            context.system( 'AimsConnectComp',
                            '-i', tmpfile,
                            '-o', tmpfile,
                            '-c', 26, '-n', 1)
            context.system( 'AimsMorphoMath',
                            '-i', tmpfile,
                            '-o', tmpfile,
                            '-m', 'clo', '-r', 1)
            mask = aims.read(tmpfile)
            mask_arr = mask.arraydata()
            
            wm_arr[mask_arr == 0] = False
            gm_arr[mask_arr == 0] = False
            csf_arr[mask_arr == 0] = False
            tiv_arr[mask_arr == 0] = False
            #Calculation of the volumes
            wm_vol = wm_arr.sum()*vox_vol/1000.
            gm_vol = gm_arr.sum()*vox_vol/1000.
            csf_vol = csf_arr.sum()*vox_vol/1000.
            tiv = tiv_arr.sum()*vox_vol/1000.

        #Write in the output file
        f.write(subject+","+
                str(round(gm_vol,3))+","+
                str(round(wm_vol,3))+","+
                str(round(csf_vol,3))+","+
                str(round(tiv,3))+"\n")

    context.progress(nb, nb, process=self)
    f.close()
    
