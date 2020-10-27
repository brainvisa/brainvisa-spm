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
import os
from soma.spm.spm_launcher import SPM12, SPM12Standalone
import gzip
import os
import shutil


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
name = 'CAT12 - Segment'
input_section = 'Inputs'
option_section = 'Initial options'
seg_options_section = 'Segmentations options'
spatial_options_section = 'Spatial registration options'
extended_section = 'Extended options'
surface_options = 'Surface options'
admin_options = 'Administration options'
output_section = 'Outputs'
grey_output = 'Grey matter'
white_output = 'White matter'
csf_output = 'CSF matter'
wmh_output = 'White matter intensity'
other_tissue_output = 'Other tissues (skull+scalp+background)'
pve_labels_output = 'PVE labels'
bias_output = 'Bias corrections'
other_output = "Other outputs"

signature = Signature(
    "t1mri", ReadDiskItem('Raw T1 MRI', ['NIFTI-1 image', 'SPM image', 'MINC image', 'gz compressed NIFTI-1 image'],
                          section=input_section),
    
    # --- Options ---
    "template", ReadDiskItem('TPM template', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                             section=option_section),
    "affine_regularisation", Choice(('ICBM European brains', 'european'),
                                    ('ICBM East Asian brains', 'east_asian'),
                                    ('No regularisation', 'no_regularisation'),
                                    ('No affine registration', 'no_registration'),
                                    section=option_section),
    "inhomogeneity_correction", Choice('ultralight', 'light', 'medium', 'strong', 'heavy',
                                       section=option_section),  # detail more the choice text with values ?
    "processing_accuracy", Choice('average', 'high', 'ultra_high',
                                  section=option_section),
    
    # --- Extended options ---
    # - Segmentation options -
    "affine_preprocessing", Choice('none', 'light', 'full', 'default', 'rough',
                                   section=seg_options_section),
    "noise_correction", Choice('none', 'classic', 'light', 'medium',
                               section=seg_options_section),  # , 'strong'),
    # "initial_segmentation", Choice('SPM unified Segmentation', 'k-means AMAP'),
    "local_adaptative_segmentation", Choice('none', 'ultralight', 'light', 'medium', 'strong', 'heavy',
                                            section=seg_options_section),
    "skull_stripping", Choice(('none', 'none'),
                              ('SPM approach', 'spm'),
                              ('GCUT approach', 'gcut_medium'),
                              ('APRG approach', 'aprg'),
                              ('APRG approach V2', 'aprg_v2'),
                              ('APRG approach V2 wider', 'aprg_v2_wider'),
                              ('APRG approach V2 tighter', 'aprg_v2_tighter'),
                              section=seg_options_section),
    "clean_up", Choice('none', 'light', 'medium', 'strong', 'heavy',
                       section=seg_options_section),
    "wm_hyperintensities_correction", Choice(("no WMH correction", "no"),
                                             ("set WMH temporary as WM", "temporary"),
                                             #  ("set WMH as WM", "save"),
                                             section=seg_options_section),
    # "stroke_lesion_correction", Choice(),
    "optimal_resolution", Choice(('Optimal resolution', 'optimal'),
                                 ('Native resolution', 'native'),
                                 ('Best native resolution', 'best'),
                                 ('Fixed resolution', 'fixed'),
                                 section=seg_options_section),
    "optimal_resolution_value", ListOf(Float(),
                                       section=seg_options_section),
    
    # - Spatial registration -
    "spatial_registration_method", Choice('shooting', 'dartel',
                                          section=spatial_options_section),
    "spatial_registration_template", ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'],
                                                  section=spatial_options_section),
    "shooting_method", Choice(("Default Shooting", 'default'),
                              ("Optimized Shooting - vox", 'opt_vox'),
                              ("Optimized Shooting - fast", 'opt_fast'),
                              ("Optimized Shooting - standard", 'opt_standard'),
                              ("Optimized Shooting - fine", 'opt_fine'),
                              ("Optimized Shooting - strong", 'opt_strong'),
                              ("Optimized Shooting - medium", 'opt_medium'),
                              ("Optimized Shooting - soft", 'opt_soft'),
                              section=spatial_options_section),
    
    "voxel_size", Float(section=extended_section),
    
    # - Surface otions - ?
    "surface_thickness_estimation", Boolean(section=surface_options),
    "voxel_size_thickness_est", Float(section=surface_options),
    "cortical_myelination_corr", Boolean(section=surface_options),
    "cortical_surf_creation", Float(section=surface_options),
    "parahipp_surf_creation", Float(section=surface_options),
    "closing_parahipp", Boolean(section=surface_options),
    
    # - Admin options -
    "create_report", Boolean(section=admin_options),
    "lazy_processing", Boolean(section=admin_options),
    "error_handling", Boolean(section=admin_options),
    "verbose", Choice('none', 'default', 'details',
                      section=admin_options),
    
    # --- Writing options ---
    # ROI process
    # ...
    # "ROI_process", Choice("No ROI processings", "Atlases",
    #                       section=output_section),
    
    "grey_native_space", Boolean(section=grey_output),
    "grey_native", WriteDiskItem('T1 MRI tissue probability map',
                                 ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                 requiredAttributes={'tissue_class': 'grey',
                                                     'transformation': 'none',
                                                     'modulation': 'none',
                                                     'warping_method': 'none',
                                                     'processing': 'cat12Segment',
                                                     'analysis': 'default'},
                                 section=grey_output),
    "grey_normalized", Boolean(section=grey_output),
    "grey_modulated_normalized", Choice(("no", 'no'),
                                        ("affine + non-linear", 'affine_non_linear'),
                                        ("non-linear only", 'non_linear'),
                                        section=grey_output),
    "grey_dartel_export", Choice("no", "rigid", "affine", "both",
                                 section=grey_output),
    
    "white_native_space", Boolean(section=white_output),
    "white_native", WriteDiskItem('T1 MRI tissue probability map',
                                  ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                  requiredAttributes={'tissue_class': 'white',
                                                      'transformation': 'none',
                                                      'modulation': 'none',
                                                      'warping_method': 'none',
                                                      'processing': 'cat12Segment',
                                                      'analysis': 'default'},
                                  section=white_output),
    "white_normalized", Boolean(section=white_output),
    "white_modulated_normalized", Choice(("no", 'no'),
                                         ("affine + non-linear", 'affine_non_linear'),
                                         ("non-linear only", 'non_linear'),
                                         section=white_output),
    "white_dartel_export", Choice("no", "rigid", "affine", "both",
                                  section=white_output),
    
    "csf_native_space", Boolean(section=csf_output),
    "csf_native", WriteDiskItem('T1 MRI tissue probability map',
                                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                requiredAttributes={'tissue_class': 'csf',
                                                    'transformation': 'none',
                                                    'modulation': 'none',
                                                    'warping_method': 'none',
                                                    'processing': 'cat12Segment',
                                                    'analysis': 'default'},
                                  section=csf_output),
    "csf_normalized", Boolean(section=csf_output),
    "csf_modulated_normalized", Choice(("no", 'no'),
                                       ("affine + non-linear", 'affine_non_linear'),
                                       ("non-linear only", 'non_linear'),
                                       section=csf_output),
    "csf_dartel_export", Choice("no", "rigid", "affine", "both",
                                section=csf_output),
    
    # "wmh_native_space", Boolean(section=wmh_output),
    # "wmh_normalized", Boolean(section=wmh_output),
    # "wmh_modulated_normalized", Choice(("no", 'no'),
    #                                    ("affine + non-linear", 'affine_non_linear'),
    #                                    ("non-linear only", 'non_linear'),
    #                                    section=wmh_output),
    # "wmh_dartel_export", Choice("no", "rigid", "affine", "both",
    #                             section=wmh_output),
    
    # "sls_native_space", Boolean(),
    # "sls_normalized", Boolean(),
    # "sls_modulated_normalized", Choice("no", "affine + non-linear", "non-linear only"),
    # "sls_dartel_export", Choice("no", "rigid", "affine", "both"),
    
    "other_tissue_proba_map_native_space", Boolean(section=other_tissue_output),
    "skull_native", WriteDiskItem('T1 MRI tissue probability map',
                                  ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                  requiredAttributes={'tissue_class': 'skull',
                                                      'transformation': 'none',
                                                      'modulation': 'none',
                                                      'warping_method': 'none',
                                                      'processing': 'cat12Segment',
                                                      'analysis': 'default'},
                                  section=other_tissue_output),
    "scalp_native", WriteDiskItem('T1 MRI tissue probability map',
                                  ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                  requiredAttributes={'tissue_class': 'scalp',
                                                      'transformation': 'none',
                                                      'modulation': 'none',
                                                      'warping_method': 'none',
                                                      'processing': 'cat12Segment',
                                                      'analysis': 'default'},
                                  section=other_tissue_output),
    "background_native", WriteDiskItem('T1 MRI tissue probability map',
                                       ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                       requiredAttributes={'tissue_class': 'none',
                                                           'transformation': 'none',
                                                           'modulation': 'none',
                                                           'warping_method': 'none',
                                                           'processing': 'cat12Segment',
                                                           'analysis': 'default'},
                                       section=other_tissue_output),
    "other_tissue_proba_map_normalized", Boolean(section=other_tissue_output),
    "other_tissue_proba_map_modulated_normalized", Choice(("no", 'no'),
                                                          ("affine + non-linear", 'affine_non_linear'),
                                                          ("non-linear only", 'non_linear'),
                                                          section=other_tissue_output),
    "other_tissue_proba_map_dartel_export", Choice("no", "rigid", "affine", "both",
                                                   section=other_tissue_output),
    
    # "roi_evaluation_native_space", Boolean(),
    # "roi_evaluation_dartel_export", Choice("no", "rigid", "affine", "both"),
    
    "pve_labels_native_space", Boolean(section=pve_labels_output),
    "pve_labels_normalized", Boolean(section=pve_labels_output),
    "pve_labels_dartel_export", Choice("no", "rigid", "affine", "both",
                                       section=pve_labels_output),
    
    "bias_native_space", Boolean(section=bias_output),
    "bias_normalized", Boolean(section=bias_output),
    "bias_dartel_export", Choice("no", "rigid", "affine", "both",
                                 section=bias_output),
    
    "local_bias_native_space", Boolean(section=bias_output),
    "local_bias_normalized", Boolean(section=bias_output),
    "local_bias_dartel_export", Choice("no", "rigid", "affine", "both",
                                       section=bias_output),
    
    "jacobian_determinant", Boolean(section=other_output),
    'deformation_field_type', Choice("Neither", 'Inverse', 'Forward', 'Inverse + Forward',
                                     section=other_output),
    "forward_field", WriteDiskItem('SPM deformation field',
                                   ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                   requiredAttributes={'direction': 'forward',
                                                       'warping_method': 'none',
                                                       'processing': 'cat12Segment',
                                                       'analysis': 'default'},
                                   section=other_output),
    "inverse_field", WriteDiskItem('SPM deformation field',
                                   ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                                   requiredAttributes={'direction': 'inverse',
                                                       'warping_method': 'none',
                                                       'processing': 'cat12Segment',
                                                       'analysis': 'default'},
                                   section=other_output),
    "registration_matrix", Boolean(section=other_output),
    "forward_registration_affine", WriteDiskItem("SPM transformation", ['Matlab file'],
                                                 requiredAttributes={'direction': 'forward',
                                                                     'transformation': 'affine',
                                                                     'processing': 'cat12Segment',
                                                                     'analysis': 'default'},
                                                 section=other_output),
    "inverse_registration_affine", WriteDiskItem("SPM transformation", ['Matlab file'],
                                                 requiredAttributes={'direction': 'inverse',
                                                                     'transformation': 'affine',
                                                                     'processing': 'cat12Segment',
                                                                     'analysis': 'default'},
                                                 section=other_output),
    "forward_registration_rigid", WriteDiskItem("SPM transformation", ['Matlab file'],
                                                requiredAttributes={'direction': 'forward',
                                                                    'transformation': 'rigid',
                                                                    'processing': 'cat12Segment',
                                                                    'analysis': 'default'},
                                                section=other_output),
    "inverse_registration_rigid", WriteDiskItem("SPM transformation", ['Matlab file'],
                                                requiredAttributes={'direction': 'inverse',
                                                                    'transformation': 'rigid',
                                                                    'processing': 'cat12Segment',
                                                                    'analysis': 'default'},
                                                section=other_output),
    
    # "output_options", Choice(("Source directory", 'source'),
    #                          ("Custom output directory", 'custom'),
    #                          section=other_output),
    # "output_directory", WriteDiskItem('Directory', 'Directory',
    #                                   section=other_output),
    "batch_location", WriteDiskItem('Matlab SPM script', 'Matlab script',
                                    section=other_output),
    
)


def initialization(self):
    self.setOptional('template', 'voxel_size', 'spatial_registration_template')
    
    self.addLink('batch_location', 't1mri', self.update_batch_path)
    self.addLink(None, 'surface_thickness_estimation', self.update_surface_selection)
    
    self.inhomogeneity_correction = 'medium'
    self.processing_accuracy = 'average'
    
    self.affine_preprocessing = 'default'
    self.noise_correction = 'medium'
    self.local_adaptative_segmentation = 'medium'
    self.skull_stripping = 'aprg'
    self.clean_up = 'medium'
    self.wm_hyperintensities_correction = 'temporary'
    self.addLink(None, 'optimal_resolution', self.update_optimal_resolution_choice)
    self.optimal_resolution = 'optimal'
    self.optimal_resolution_value = [1, 0.1]
    self.addLink(None, 'spatial_registration_method', self.update_registration_method)
    self.spatial_registration_method = 'shooting'
    self.shooting_method = 'opt_standard'
    self.voxel_size = 1.5
    
    self.voxel_size_thickness_est = 0.5
    self.cortical_myelination_corr = False
    self.cortical_surf_creation = 0.7
    self.parahipp_surf_creation = 0.1
    self.closing_parahipp = False
    
    self.create_report = True
    self.lazy_processing = False
    self.error_handling = True
    self.verbose = 'details'
    
    # self.ROI_process = 'No ROI processings'
    
    self.grey_native_space = False
    self.grey_normalized = False
    self.grey_modulated_normalized = 'affine_non_linear'
    self.grey_dartel_export = 'no'
    
    self.white_native_space = False
    self.white_normalized = False
    self.white_modulated_normalized = 'affine_non_linear'
    self.white_dartel_export = 'no'
    
    self.csf_native_space = False
    self.csf_normalized = False
    self.csf_modulated_normalized = 'no'
    self.csf_dartel_export = 'no'

    # self.wmh_native_space = False
    # self.wmh_normalized = False
    # self.wmh_modulated_normalized = 'no'
    # self.wmh_dartel_export = 'no'

    self.other_tissue_proba_map_native_space = False
    self.other_tissue_proba_map_normalized = False
    self.other_tissue_proba_map_modulated_normalized = 'no'
    self.other_tissue_proba_map_dartel_export = 'no'
    
    self.pve_labels_native_space = True
    self.pve_labels_normalized = False
    self.pve_labels_dartel_export = 'no'

    self.bias_native_space = False
    self.bias_normalized = True
    self.bias_dartel_export = 'no'

    self.local_bias_native_space = False
    self.local_bias_normalized = False
    self.local_bias_dartel_export = 'no'
    
    self.jacobian_determinant = False
    self.deformation_field_type = 'Neither'
    self.registration_matrix = False
    
    self.addLink(None, 'output_options', self.update_output_dir)
    
    self.addLink(None, 'grey_native_space', lambda x: self.update_bool_output_signature(x, 'grey_native'))
    self.addLink(None, 'white_native_space', lambda x: self.update_bool_output_signature(x, 'white_native'))
    self.addLink(None, 'csf_native_space', lambda x: self.update_bool_output_signature(x, 'csf_native'))
    self.addLink(None, 'other_tissue_proba_map_native_space',
                 lambda x: self.update_bool_output_signature(x, 'skull_native'))
    self.addLink(None, 'other_tissue_proba_map_native_space',
                 lambda x: self.update_bool_output_signature(x, 'scalp_native'))
    self.addLink(None, 'other_tissue_proba_map_native_space',
                 lambda x: self.update_bool_output_signature(x, 'background_native'))
    self.addLink(None, 'deformation_field_type', self.update_deformation_field_signature)
    self.addLink(None, 'registration_matrix', lambda x: self.update_bool_output_signature(x, 'forward_registration_affine'))
    self.addLink(None, 'registration_matrix', lambda x: self.update_bool_output_signature(x, 'inverse_registration_affine'))
    self.addLink(None, 'registration_matrix', lambda x: self.update_bool_output_signature(x, 'forward_registration_rigid'))
    self.addLink(None, 'registration_matrix', lambda x: self.update_bool_output_signature(x, 'inverse_registration_rigid'))
    
    self.addLink('grey_native', 't1mri')
    self.addLink('white_native', 't1mri')
    self.addLink('csf_native', 't1mri')
    self.addLink('skull_native', 't1mri')
    self.addLink('scalp_native', 't1mri')
    self.addLink('background_native', 't1mri')
    self.addLink('forward_field', 't1mri')
    self.addLink('inverse_field', 't1mri')
    self.addLink('forward_registration_affine', 't1mri')
    self.addLink('inverse_registration_affine', 't1mri')
    self.addLink('forward_registration_rigid', 't1mri')
    self.addLink('inverse_registration_rigid', 't1mri')


def _test(self, proc):
    attr = self.t1mri.hierarchyAttributes()
    with open('/tmp/log.log', 'w') as log_file:
        print(self.signature['inverse_field'].requiredAttributes)
        d = self.signature['inverse_field'].findValue(attr,
                                                      _debug=log_file)
        self.signature['inverse_registration_rigid'].findValue(attr,
                                                               _debug=log_file)
        print('DDD', d)


def update_batch_path(self, proc):
    if self.t1mri is not None:
        directory_path = os.path.dirname(self.t1mri.fullPath())
        return os.path.join(directory_path, 'cat12_segment_job.m')


def update_surface_selection(self, proc):
    if self.surface_thickness_estimation:
        self.setEnable("voxel_size_thickness_est", "cortical_myelination_corr",
                       "cortical_surf_creation", "parahipp_surf_creation",
                       "closing_parahipp",)
    else:
        self.setDisable("voxel_size_thickness_est", "cortical_myelination_corr",
                        "cortical_surf_creation", "parahipp_surf_creation",
                        "closing_parahipp",)
    self.changeSignature(self.signature)
        

def update_registration_method(self, proc):
    if self.spatial_registration_method == 'shooting':
        self.setEnable('shooting_method')
    elif self.spatial_registration_method == 'dartel':
        self.setDisable('shooting_method')
    self.changeSignature(self.signature)
        

def update_optimal_resolution_choice(self, proc):
    if self.optimal_resolution == 'native':
        self.setDisable('optimal_resolution_value')
    else:
        self.setEnable('optimal_resolution_value')
    self.changeSignature(self.signature)
        

def update_output_dir(self, proc):
    if self.output_options == 'source':
        self.setDisable('output_directory')
    else:
        self.setEnable('output_directory')
    self.changeSignature(self.signature)


def update_bool_output_signature(self, proc, d):
    if proc:
        self.setEnable(d)
    else:
        self.setDisable(d)
    self.changeSignature(signature)


def update_deformation_field_signature(self, proc):
    if 'Forward' in proc:
        self.setEnable('forward_field')
    else:
        self.setDisable('forward_field')
        
    if 'Inverse' in proc:
        self.setEnable('inverse_field')
    else:
        self.setDisable('inverse_field')
    self.changeSignature(signature)
    
    
def execution(self, context):
    t1mri_path = self.t1mri.fullPath()
    delete_t1 = False
    if t1mri_path.endswith('.gz'):
        t1mri_unzip_path = t1mri_path[:-3]
        if os.path.exists(t1mri_unzip_path):
            t1mri_unzip_path = t1mri_unzip_path.replace('.nii', '_unziped.nii')
        with gzip.open(t1mri_path, 'rb') as t1mri:
            with open(t1mri_unzip_path, 'wb') as t1mri_unzip:
                shutil.copyfileobj(t1mri, t1mri_unzip)
        delete_t1 = True
        t1mri_path = t1mri_unzip_path
    
    output_path = os.path.dirname(os.path.dirname(self.grey_native.fullPath()))
    print('OUTPUT', output_path)
    
    context.runProcess('SPM12CAT12Segment_generic',
                       t1mri=t1mri_path,
                       template=self.template,
                       affine_regularisation=self.affine_regularisation,
                       inhomogeneity_correction=self.inhomogeneity_correction,
                       processing_accuracy=self.processing_accuracy,
                       affine_preprocessing=self.affine_preprocessing,
                       noise_correction=self.noise_correction,
                       local_adaptative_segmentation=self.local_adaptative_segmentation,
                       skull_stripping=self.skull_stripping,
                       clean_up=self.clean_up,
                       wm_hyperintensities_correction=self.wm_hyperintensities_correction,
                       optimal_resolution=self.optimal_resolution,
                       optimal_resolution_value=self.optimal_resolution_value,
                       spatial_registration_method=self.spatial_registration_method,
                       spatial_registration_template=self.spatial_registration_template,
                       shooting_method=self.shooting_method,
                       voxel_size=self.voxel_size,
                       surface_thickness_estimation=self.surface_thickness_estimation,
                       voxel_size_thickness_est=self.voxel_size_thickness_est,
                       cortical_myelination_corr=self.cortical_myelination_corr,
                       cortical_surf_creation=self.cortical_surf_creation,
                       parahipp_surf_creation=self.parahipp_surf_creation,
                       closing_parahipp=self.closing_parahipp,
                       create_report=self.create_report,
                       lazy_processing=self.lazy_processing,
                       error_handling=self.error_handling,
                       verbose=self.verbose,
                       grey_native_space=self.grey_native_space,
                       grey_normalized=self.grey_normalized,
                       grey_modulated_normalized=self.grey_modulated_normalized,
                       grey_dartel_export=self.grey_dartel_export,
                       white_native_space=self.white_native_space,
                       white_normalized=self.white_normalized,
                       white_modulated_normalized=self.white_modulated_normalized,
                       white_dartel_export=self.white_dartel_export,
                       csf_native_space=self.csf_native_space,
                       csf_normalized=self.csf_normalized,
                       csf_modulated_normalized=self.csf_modulated_normalized,
                       csf_dartel_export=self.csf_dartel_export,
                       other_tissue_proba_map_native_space=self.other_tissue_proba_map_native_space,
                       other_tissue_proba_map_normalized=self.other_tissue_proba_map_normalized,
                       other_tissue_proba_map_modulated_normalized=self.other_tissue_proba_map_modulated_normalized,
                       other_tissue_proba_map_dartel_export=self.other_tissue_proba_map_dartel_export,
                       pve_labels_native_space=self.pve_labels_native_space,
                       pve_labels_normalized=self.pve_labels_normalized,
                       pve_labels_dartel_export=self.pve_labels_dartel_export,
                       bias_native_space=self.bias_native_space,
                       bias_normalized=self.bias_normalized,
                       bias_dartel_export=self.bias_dartel_export,
                       local_bias_native_space=self.local_bias_native_space,
                       local_bias_normalized=self.local_bias_normalized,
                       local_bias_dartel_export=self.local_bias_dartel_export,
                       jacobian_determinant=self.jacobian_determinant,
                       deformation_field_type=self.deformation_field_type,
                       registration_matrix=self.registration_matrix,
                       output_options='custom',
                       output_directory=output_path,
                       batch_location=self.batch_location)

    if delete_t1:
        os.remove(t1mri_path)
