# -*- coding: utf-8 -*-
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem
from brainvisa.processes import Choice
from soma import aims, aimsalgo
from pathlib import Path
import numpy as np


name = 'SPM - Brain Tissues Volumes'
userLevel = 0

signature = Signature(
    'white_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'white',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'white_warped_unmodulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'white',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'low-dimensional'}),
    'white_warped_modulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'white',
                            'transformation': 'none',
                            'modulation': 'affine and non-linear',
                            'warping_method': 'low-dimensional'}),
    'grey_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'grey',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'grey_warped_unmodulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'grey',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'low-dimensional'}),
    'grey_warped_modulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'grey',
                            'transformation': 'none',
                            'modulation': 'affine and non-linear',
                            'warping_method': 'low-dimensional'}),
    'csf_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'csf',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'csf_warped_unmodulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'csf',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'low-dimensional'}),
    'csf_warped_modulated_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'csf',
                            'transformation': 'none',
                            'modulation': 'affine and non-linear',
                            'warping_method': 'low-dimensional'}),
    'skull_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'skull',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'scalp_proba_map', ReadDiskItem(
        'T1 MRI tissue probability map',
        'Aims readable volume formats',
        requiredAttributes={'tissue_class': 'scalp',
                            'transformation': 'none',
                            'modulation': 'none',
                            'warping_method': 'none'}),
    'mode', Choice(('Sum of the native images (CAT)', 'native'),
                   ('Sum of the wm images', 'default'),
                   ('Sum of the wm images + TIV mask (Malone)', 'default+mask'),
                   ('Sum of the wm images + individual TIV mask', 'default+ind_mask'),
                   ('Probability maximum', 'proba_max')),
    'tiv_mask', ReadDiskItem(
        'Label Volume',
        'Aims readable volume formats'),
    'tissues_volumes_file', WriteDiskItem('CSV File', 'CSV File')
)


def initialization(self):
    def link_csv(self, proc):
        if self.grey_proba_map:
            d = Path(self.grey_proba_map.fullPath()).parent
            p = Path(d, 'tissues_volumes_spm.csv')
            return p.as_posix()

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
    self.linkParameters('tissues_volumes_file', 'grey_proba_map', link_csv)
    self.mode = 'default'
    self.setOptional('white_warped_unmodulated_proba_map')
    self.setOptional('white_warped_modulated_proba_map')
    self.setOptional('grey_warped_unmodulated_proba_map')
    self.setOptional('grey_warped_modulated_proba_map')
    self.setOptional('csf_warped_unmodulated_proba_map')
    self.setOptional('csf_warped_modulated_proba_map')
    self.setOptional('skull_proba_map')
    self.setOptional('scalp_proba_map')
    self.setOptional('tiv_mask')


def execution(self, context):
    f = open(self.tissues_volumes_file.fullPath(), 'w')
    f.write('subject,grey,white,csf,tiv\n')
    subject = self.white_proba_map.get('subject')

    if self.mode == 'default+ind_mask':
        #Compute an approximate intracranial mask from normalized images
        white_w = aims.read(self.white_warped_unmodulated_proba_map.fullPath())
        grey_w = aims.read(self.grey_warped_unmodulated_proba_map.fullPath())
        csf_w = aims.read(self.csf_warped_unmodulated_proba_map.fullPath())
        tiv_mask = white_w + grey_w + csf_w
        tiv_mask.astype('int16')  # e > 0.5 = 1
    elif self.mode == 'default+mask':
        tiv_mask = aims.read(self.tiv_mask.fullPath())

    if self.mode == 'default' or self.mode == 'default+mask' or self.mode == 'default+ind_mask':
        white_mw = aims.read(self.white_warped_modulated_proba_map.fullPath())
        grey_mw = aims.read(self.grey_warped_modulated_proba_map.fullPath())
        csf_mw = aims.read(self.csf_warped_modulated_proba_map.fullPath())
        tiv_mw = white_mw + grey_mw + csf_mw

        if self.mode == 'default+mask' or self.mode == 'default+ind_mask':
            white_mw[np.where(tiv_mask.np == 0)] = 0.
            grey_mw[np.where(tiv_mask.np == 0)] = 0.
            csf_mw[np.where(tiv_mask.np == 0)] = 0.
            tiv_mw[np.where(tiv_mask.np == 0)] = 0.
            # Not sure if it is still necessary
            # white_mw[np.where(np.isnan(white_mw))] = 0.
            # grey_mw[np.where(np.isnan(grey_mw))] = 0.
            # csf_mw[np.where(np.isnan(csf_mw))] = 0.
            # tiv_mw[np.where(np.isnan(tiv_mw))] = 0.
            # white_mw[np.where(white_mw.np < 0.)] = 0.
            # grey_mw[np.where(grey_mw.np < 0.)] = 0.
            # csf_mw[np.where(csf_mw.np < 0.)] = 0.
            # tiv_mw[np.where(tiv_mw.np < 0.)] = 0.

        tiv = compute_vol(tiv_mw)
        wm_vol = compute_vol(white_mw)
        gm_vol = compute_vol(grey_mw)
        csf_vol = compute_vol(csf_mw)

    elif self.mode == 'native':
        white = aims.read(self.white_proba_map.fullPath())
        grey = aims.read(self.grey_proba_map.fullPath())
        csf = aims.read(self.csf_proba_map.fullPath())
        tiv = white + grey + csf

        tiv = compute_vol(tiv)
        wm_vol = compute_vol(white)
        gm_vol = compute_vol(grey)
        csf_vol = compute_vol(csf)

    elif self.mode == 'proba_max':
        tmp_w = context.temporary('gz compressed NIFTI-1 image')
        context.runProcess('computeOneTissueMask',
                           native_prob_map=self.white_proba_map,
                           others_prob_maps=[self.grey_proba_map, self.csf_proba_map,
                                             self.skull_proba_map, self.scalp_proba_map],
                           native_mask=tmp_w,
                           resolve_equal_probability=True)
        tmp_g = context.temporary('gz compressed NIFTI-1 image')
        context.runProcess('computeOneTissueMask',
                           native_prob_map=self.grey_proba_map,
                           others_prob_maps=[self.white_proba_map, self.csf_proba_map,
                                             self.skull_proba_map, self.scalp_proba_map],
                           native_mask=tmp_g,
                           resolve_equal_probability=True)
        tmp_c = context.temporary('gz compressed NIFTI-1 image')
        context.runProcess('computeOneTissueMask',
                           native_prob_map=self.csf_proba_map,
                           others_prob_maps=[self.grey_proba_map, self.white_proba_map,
                                             self.skull_proba_map, self.scalp_proba_map],
                           native_mask=tmp_c,
                           resolve_equal_probability=True)
        white = aims.read(tmp_w.fullPath(), border=2)
        grey = aims.read(tmp_g.fullPath(), border=2)
        csf = aims.read(tmp_c.fullPath(), border=2)
        tiv = white + grey + csf
        aims.AimsConnectedComponent(tiv, aims.Connectivity.CONNECTIVITY_26_XYZ,
                                    0, True, 0, 0, 1)
        cltiv = aimsalgo.AimsMorphoClosing(tiv, 1)
        white[np.where(cltiv.np == 0)] = 0
        grey[np.where(cltiv.np == 0)] = 0
        csf[np.where(cltiv.np == 0)] = 0

        tiv = compute_vol(tiv)
        wm_vol = compute_vol(white)
        gm_vol = compute_vol(grey)
        csf_vol = compute_vol(csf)

    #Write in the output file
    f.write(f'{subject},{str(gm_vol)},{str(wm_vol)},{str(csf_vol)},{str(tiv)}\n')
    f.close()


def compute_vol(map):
    vox_sizes = map.header()['voxel_size']
    vox_vol = vox_sizes[0] * vox_sizes[1] * vox_sizes[2]
    vol = map.np.sum() * vox_vol / 1000.
    return round(vol, 3)
